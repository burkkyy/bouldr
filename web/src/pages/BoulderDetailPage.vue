<template>
  <div>
    <v-btn
      variant="text"
      prepend-icon="mdi-arrow-left"
      :to="{ name: 'BouldersPage' }"
      class="mb-4"
    >
      Back to Boulders
    </v-btn>

    <v-skeleton-loader v-if="isLoading" type="article" />

    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

    <template v-else-if="boulder">
      <h1 class="text-h4 mb-2">{{ boulder.name }}</h1>

      <div class="d-flex align-center ga-2 mb-4">
        <v-chip color="primary">Grade {{ boulder.grade }}</v-chip>
        <span v-if="boulder.coordinates" class="text-body-2 text-medium-emphasis">
          <v-icon size="small">mdi-map-marker</v-icon>
          {{ boulder.coordinates }}
        </span>
      </div>

      <p v-if="boulder.description" class="text-body-1 mb-6">{{ boulder.description }}</p>

      <v-img
        v-if="boulder.image"
        :src="boulder.image"
        max-height="300"
        class="rounded mb-6"
        cover
      />

      <h2 class="text-h5 mb-4">Sends</h2>

      <v-skeleton-loader v-if="sendsLoading" type="list-item-three-line" />

      <div v-else-if="sends.length > 0" class="d-flex flex-column ga-3">
        <v-card v-for="send in sends" :key="send.id" variant="outlined">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <span class="font-weight-medium">{{ send.displayName || send.username || `User #${send.userId}` }}</span>
                <v-chip size="x-small" :color="send.sendType === 1 ? 'success' : 'info'" class="ml-2">
                  {{ send.sendType === 1 ? 'Flash' : 'Send' }}
                </v-chip>
              </div>
              <div v-if="send.rating != null" class="d-flex align-center">
                <v-icon size="small" color="amber">mdi-star</v-icon>
                <span class="ml-1 text-body-2">{{ send.rating }} / 5</span>
              </div>
            </div>
            <div class="text-caption text-medium-emphasis mt-1">
              {{ formatDate(send.createdAt) }}
            </div>
          </v-card-text>
        </v-card>
      </div>

      <v-empty-state
        v-else
        icon="mdi-emoticon-sad-outline"
        title="No sends yet"
        text="Nobody has logged a send on this boulder yet."
      />
    </template>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import bouldersApi, { type Boulder } from "@/api/boulders-api"
import sendsApi, { type Send } from "@/api/sends-api"

const route = useRoute()
const boulderId = Number(route.params.id)

const boulder = ref<Boulder | null>(null)
const sends = ref<Send[]>([])
const isLoading = ref(true)
const sendsLoading = ref(true)
const error = ref<string | null>(null)

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
}

onMounted(async () => {
  try {
    boulder.value = await bouldersApi.get(boulderId)
  } catch (e) {
    error.value = "Failed to load boulder."
    console.error(e)
  } finally {
    isLoading.value = false
  }

  try {
    sends.value = await sendsApi.list({ boulderID: boulderId })
  } catch (e) {
    console.error("Failed to load sends:", e)
  } finally {
    sendsLoading.value = false
  }
})
</script>