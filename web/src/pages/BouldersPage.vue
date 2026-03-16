<template>
  <div>
    <h1 class="text-h4 mb-6">Boulders</h1>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

    <v-row class="mb-4">
      <v-col cols="12" sm="4">
        <v-select
          v-model="selectedRegionId"
          :items="regionItems"
          label="Filter by region"
          clearable
          density="compact"
          variant="outlined"
        />
      </v-col>
    </v-row>

    <v-row v-if="isLoading">
      <v-col v-for="n in 6" :key="n" cols="12" sm="6" md="4">
        <v-skeleton-loader type="card" />
      </v-col>
    </v-row>

    <v-row v-else-if="filteredBoulders.length > 0">
      <v-col
        v-for="boulder in filteredBoulders"
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
            <v-chip size="small" color="primary" class="mt-1">
              Grade {{ boulder.grade }}
            </v-chip>
          </v-card-subtitle>
          <v-card-text>
            <p v-if="boulder.description" class="text-body-2">
              {{ boulder.description }}
            </p>
            <p v-else class="text-body-2 text-medium-emphasis">
              No description
            </p>
            <div v-if="boulder.coordinates" class="mt-2 text-caption text-medium-emphasis">
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
      title="No boulders found"
      text="There are no boulders matching your filters."
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from "vue"
import bouldersApi, { type Boulder } from "@/api/boulders-api"
import regionsApi, { type Region } from "@/api/regions-api"

const boulders = ref<Boulder[]>([])
const regions = ref<Region[]>([])
const selectedRegionId = ref<number | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)

const regionItems = computed(() => {
  const types = new Set(regions.value.map((r) => r.type))
  const items: { title: string; value: number; props?: { subtitle: string } }[] = []
  for (const type of types) {
    const regionsOfType = regions.value.filter((r) => r.type === type)
    for (const region of regionsOfType) {
      items.push({
        title: region.name,
        value: region.id,
        props: { subtitle: type },
      })
    }
  }
  return items
})

const filteredBoulders = computed(() => {
  if (selectedRegionId.value == null) return boulders.value

  // Find the selected region and all its sub regions
  const matchingIds = new Set<number>()
  matchingIds.add(selectedRegionId.value)

  // Go thru region tree to find subregions
  let added = true
  while (added) {
    added = false
    for (const region of regions.value) {
      if (region.parentId != null && matchingIds.has(region.parentId) && !matchingIds.has(region.id)) {
        matchingIds.add(region.id)
        added = true
      }
    }
  }

  return boulders.value.filter(
    (b) => b.regionId != null && matchingIds.has(b.regionId)
  )
})

onMounted(async () => {
  try {
    const [bouldersData, regionsData] = await Promise.all([
      bouldersApi.list(),
      regionsApi.list(),
    ])
    boulders.value = bouldersData
    regions.value = regionsData
  } catch (e) {
    error.value = "Failed to load boulders."
    console.error(e)
  } finally {
    isLoading.value = false
  }
})
</script>
