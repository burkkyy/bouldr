<template>
  <div>
    <div class="d-flex align-center mb-6">
      <h1 class="text-h4">Boulders</h1>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-plus" @click="showCreateDialog = true">
        Create Boulder
      </v-btn>
    </div>

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

    <!-- Create Boulder Dialog -->
    <v-dialog v-model="showCreateDialog" max-width="600" persistent>
      <v-card>
        <v-card-title>Create Boulder</v-card-title>
        <v-card-text>
          <v-form ref="createForm" @submit.prevent="handleCreateBoulder">
            <v-text-field
              v-model="newBoulder.name"
              label="Name"
              :rules="[rules.required]"
              class="mb-2"
            />
            <v-text-field
              v-model.number="newBoulder.grade"
              label="Grade"
              type="number"
              :rules="[rules.required]"
              class="mb-2"
            />
            <v-combobox
              v-model="selectedRegion"
              :items="regionAutocompleteItems"
              label="Region"
              clearable
              class="mb-2"
              hint="Select an existing region or type a new one"
              persistent-hint
            />
            <v-select
              v-if="isNewRegion"
              v-model="newRegionType"
              :items="regionTypeOptions"
              label="New region type"
              :rules="[rules.required]"
              class="mb-2"
            />
            <v-select
              v-if="isNewRegion && newRegionType && newRegionType !== 'Country'"
              v-model="newRegionParentId"
              :items="parentRegionItems"
              label="Located in"
              clearable
              class="mb-2"
              hint="Which region does this belong to?"
              persistent-hint
            />
            <v-textarea
              v-model="newBoulder.description"
              label="Description"
              rows="3"
              class="mb-2"
            />
            <v-text-field
              v-model="newBoulder.coordinates"
              label="Coordinates"
              placeholder="e.g. 49.123, -123.456"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="resetCreateDialog">Cancel</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="isCreating"
            @click="handleCreateBoulder"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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

// Create boulder state
const showCreateDialog = ref(false)
const isCreating = ref(false)
const selectedRegion = ref<{ title: string; value: number } | string | null>(null)
const newRegionType = ref<string | null>(null)
const newRegionParentId = ref<number | null>(null)
const newBoulder = ref({
  name: "",
  grade: null as number | null,
  description: "",
  coordinates: "",
})

const rules = {
  required: (v: unknown) => (v !== null && v !== undefined && v !== "") || "Required",
}

const regionTypeOptions = ["country", "province", "area", "city"]

const regionAutocompleteItems = computed(() =>
  regions.value.map((r) => ({
    title: `${r.name} (${r.type})`,
    value: r.id,
  }))
)

const isNewRegion = computed(() => typeof selectedRegion.value === "string")

const parentRegionItems = computed(() =>
  regions.value.map((r) => ({
    title: `${r.name} (${r.type})`,
    value: r.id,
  }))
)

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

function resetCreateDialog() {
  showCreateDialog.value = false
  newBoulder.value = { name: "", grade: null, description: "", coordinates: "" }
  selectedRegion.value = null
  newRegionType.value = null
  newRegionParentId.value = null
}

async function handleCreateBoulder() {
  if (!newBoulder.value.name || newBoulder.value.grade === null) return

  isCreating.value = true
  error.value = null

  try {
    let regionId: number | null = null

    // If user typed a new region name (string), create it first
    if (typeof selectedRegion.value === "string" && selectedRegion.value.trim()) {
      if (!newRegionType.value) {
        error.value = "Please select a type for the new region."
        isCreating.value = false
        return
      }
      const newRegion = await regionsApi.create({
        type: newRegionType.value,
        name: selectedRegion.value.trim(),
        parentId: newRegionParentId.value,
      })
      regions.value.push(newRegion)
      regionId = newRegion.id
    } else if (selectedRegion.value && typeof selectedRegion.value === "object") {
      regionId = selectedRegion.value.value
    }

    const created = await bouldersApi.create({
      authorId: 1, // TODO: use actual logged-in user
      name: newBoulder.value.name,
      grade: newBoulder.value.grade,
      regionId,
      description: newBoulder.value.description || null,
      coordinates: newBoulder.value.coordinates || null,
    })

    boulders.value.push(created)
    resetCreateDialog()
  } catch (e) {
    error.value = "Failed to create boulder."
    console.error(e)
  } finally {
    isCreating.value = false
  }
}

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
