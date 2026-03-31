<template>
  <div>
    <div class="d-flex align-center mb-6">
      <h1 class="text-h4">Boulders</h1>
      <v-spacer />
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        text="Create Boulder"
        @click="openBoulderCreateDialog"
      />
    </div>

    <v-alert
      v-if="error"
      type="error"
      class="mb-4"
      >{{ error }}</v-alert
    >

    <!-- Map -->
    <div
      ref="mapContainer"
      style="height: 400px; width: 100%; border-radius: 8px; z-index: 0"
      class="mb-6"
    ></div>

    <!-- Boulder list filtered by map bounds -->
    <h2 class="text-h5 mb-4">
      {{ visibleBoulders.length }} boulder{{ visibleBoulders.length === 1 ? "" : "s" }} in view
    </h2>

    <v-row v-if="isLoading">
      <v-col
        v-for="n in 6"
        :key="n"
        cols="12"
        sm="6"
        md="4"
      >
        <v-skeleton-loader type="card" />
      </v-col>
    </v-row>

    <v-row v-else-if="visibleBoulders.length > 0">
      <v-col
        v-for="boulder in visibleBoulders"
        :key="boulder.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card
          height="100%"
          :to="{ name: 'BoulderDetailPage', params: { id: boulder.id } }"
          hover
        >
          <v-card-title>{{ boulder.name }}</v-card-title>
          <v-card-subtitle>
            <v-chip
              size="small"
              color="primary"
              class="mt-1"
            >
              V{{ boulder.grade }}
            </v-chip>
          </v-card-subtitle>
          <v-card-text>
            <p
              v-if="boulder.description"
              class="text-body-2"
            >
              {{ boulder.description }}
            </p>
            <p
              v-else
              class="text-body-2 text-medium-emphasis"
            >
              No description
            </p>
            <div
              v-if="boulder.coordinates"
              class="mt-2 text-caption text-medium-emphasis"
            >
              <v-icon size="small">mdi-map-marker</v-icon>
              {{ boulder.coordinates }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-empty-state
      v-else
      icon="mdi-image-broken-variant"
      title="No boulders in view"
      text="Pan or zoom the map to find boulders."
    />

    <BoulderCreateDialog
      ref="boulderCreateDialog"
      @created="refresh"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, onBeforeUnmount, ref, watch, nextTick } from "vue"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

import bouldersApi, { type Boulder } from "@/api/boulders-api"
import regionsApi, { type Region } from "@/api/regions-api"

import BoulderCreateDialog from "@/components/boulders/BoulderCreateDialog.vue"

const boulders = ref<Boulder[]>([])
const regions = ref<Region[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)

// Map state
const mapContainer = ref<HTMLElement | null>(null)
let map: L.Map | null = null
let markerLayer: L.LayerGroup | null = null
const mapBounds = ref<L.LatLngBounds | null>(null)

function parseCoords(coords: string): [number, number] | null {
  const match = coords.match(/^(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$/)
  if (!match) return null
  const lat = parseFloat(match[1])
  const lng = parseFloat(match[2])
  if (lat < -90 || lat > 90 || lng < -180 || lng > 180) return null
  return [lat, lng]
}

const visibleBoulders = computed(() => {
  if (!mapBounds.value) return boulders.value
  return boulders.value.filter((b) => {
    if (!b.coordinates) return false
    const parsed = parseCoords(b.coordinates)
    if (!parsed) return false
    return mapBounds.value!.contains(L.latLng(parsed[0], parsed[1]))
  })
})

function updateMarkers() {
  if (!markerLayer || !map) return
  markerLayer.clearLayers()

  for (const boulder of boulders.value) {
    if (!boulder.coordinates) continue
    const parsed = parseCoords(boulder.coordinates)
    if (!parsed) continue

    L.marker(parsed)
      .bindPopup(`<strong>${boulder.name}</strong><br>V${boulder.grade}`)
      .addTo(markerLayer)
  }
}

function initMap() {
  if (!mapContainer.value) return

  // Fix Leaflet default icon paths
  delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  })

  map = L.map(mapContainer.value).setView([49.32, -123.13], 10)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(map)

  markerLayer = L.layerGroup().addTo(map)

  const onBoundsChange = () => {
    if (map) mapBounds.value = map.getBounds()
  }
  map.on("moveend", onBoundsChange)
  map.on("zoomend", onBoundsChange)
  onBoundsChange()
}

function fitMapToBoulders() {
  if (!map) return
  const points: [number, number][] = []
  for (const b of boulders.value) {
    if (!b.coordinates) continue
    const parsed = parseCoords(b.coordinates)
    if (parsed) points.push(parsed)
  }
  if (points.length > 0) {
    map.fitBounds(L.latLngBounds(points.map((p) => L.latLng(p[0], p[1]))), { padding: [40, 40] })
  }
}

watch(
  boulders,
  () => {
    updateMarkers()
  },
  { deep: true }
)

const boulderCreateDialog = ref<InstanceType<typeof BoulderCreateDialog> | null>(null)

function openBoulderCreateDialog() {
  boulderCreateDialog.value?.show()
}

async function refresh() {
  try {
    const [bouldersData, regionsData] = await Promise.all([bouldersApi.list(), regionsApi.list()])
    boulders.value = bouldersData
    regions.value = regionsData
  } catch (e) {
    error.value = "Failed to load boulders."
    console.error(e)
  } finally {
    isLoading.value = false
  }

  await nextTick()
  updateMarkers()
  fitMapToBoulders()
}

onMounted(async () => {
  initMap()
  refresh()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>
