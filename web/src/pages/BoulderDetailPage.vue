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

    <v-skeleton-loader
      v-if="isLoading"
      type="article"
    />

    <v-alert
      v-else-if="error"
      type="error"
      >{{ error }}</v-alert
    >

    <template v-else-if="boulder">
      <v-row class="mb-6">
        <v-col
          cols="12"
          md="7"
        >
          <h1 class="text-h4 mb-2">{{ boulder.name }}</h1>

          <div class="d-flex align-center ga-2 mb-4">
            <v-chip color="primary">V{{ boulder.grade }}</v-chip>
            <span
              v-if="boulder.coordinates"
              class="text-body-2 text-medium-emphasis"
            >
              <v-icon size="small">mdi-map-marker</v-icon>
              {{ boulder.coordinates }}
            </span>
          </div>

          <p
            v-if="boulder.description"
            class="text-body-1"
          >
            {{ boulder.description }}
          </p>
        </v-col>

        <v-col
          cols="12"
          md="5"
        >
          <div class="d-flex ga-3" :class="{ 'flex-column': !boulder.coordinates }">
            <div :style="boulder.coordinates ? 'flex: 1; min-width: 0' : ''">
              <a
                v-if="boulder.image"
                :href="imageUrl"
                target="_blank"
              >
                <v-card
                  class="overflow-hidden"
                  rounded="lg"
                  elevation="2"
                  style="cursor: pointer"
                >
                  <v-img
                    :src="imageUrl"
                    :max-height="boulder.coordinates ? 200 : 200"
                    contain
                    class="bg-grey-darken-4"
                  />
                </v-card>
              </a>
              <div
                v-else
                class="d-flex align-center justify-center bg-grey-lighten-3 rounded-lg"
                style="height: 200px"
              >
                <v-icon
                  size="64"
                  color="grey-lighten-1"
                >
                  mdi-image-filter-hdr
                </v-icon>
              </div>
            </div>
            <div
              v-if="boulder.coordinates"
              style="flex: 1; min-width: 0"
            >
              <v-card
                rounded="lg"
                elevation="2"
                class="overflow-hidden"
              >
                <div
                  ref="detailMapContainer"
                  style="height: 200px; width: 100%"
                ></div>
              </v-card>
            </div>
          </div>
        </v-col>
      </v-row>

      <div class="d-flex align-center justify-space-between mb-4">
        <h2 class="text-h5">Sends</h2>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="onLogSendClick"
        >
          Log Send
        </v-btn>
      </div>

      <v-dialog
        v-model="showLoginDialog"
        max-width="400"
      >
        <v-card title="Sign in to log a send">
          <v-card-text>
            <v-text-field
              v-model="loginUsername"
              label="Username"
              variant="outlined"
              :error-messages="loginError"
              @keyup.enter="handleLogin"
            />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn
              variant="text"
              @click="showLoginDialog = false"
              >Cancel</v-btn
            >
            <v-btn
              color="primary"
              :loading="loginLoading"
              :disabled="!loginUsername.trim()"
              @click="handleLogin"
            >
              Sign In
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="showLogSendDialog"
        max-width="400"
      >
        <v-card title="Log a Send">
          <v-card-text>
            <v-select
              v-model="newSend.sendType"
              :items="[
                { title: 'Flash', value: 1 },
                { title: 'Send', value: 2 },
              ]"
              label="Send Type"
              variant="outlined"
              class="mb-3"
            />
            <v-slider
              v-model="newSend.rating"
              :min="0"
              :max="5"
              :step="0.5"
              label="Rating"
              thumb-label
              color="amber"
            />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn
              variant="text"
              @click="showLogSendDialog = false"
              >Cancel</v-btn
            >
            <v-btn
              color="primary"
              :loading="sendSubmitting"
              @click="submitSend"
              >Submit</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-skeleton-loader
        v-if="sendsLoading"
        type="list-item-three-line"
      />

      <div
        v-else-if="sends.length > 0"
        class="d-flex flex-column ga-3"
      >
        <v-card
          v-for="send in sends"
          :key="send.id"
          variant="outlined"
        >
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <span class="font-weight-medium">{{
                  send.displayName || send.username || `User #${send.userId}`
                }}</span>
                <v-chip
                  size="x-small"
                  :color="send.sendType === 1 ? 'success' : 'info'"
                  class="ml-2"
                >
                  {{ send.sendType === 1 ? "Flash" : "Send" }}
                </v-chip>
              </div>
              <div
                v-if="send.rating != null"
                class="d-flex align-center"
              >
                <v-icon
                  size="small"
                  color="amber"
                  >mdi-star</v-icon
                >
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
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

import bouldersApi, { type Boulder } from "@/api/boulders-api"
import sendsApi, { type Send } from "@/api/sends-api"
import { API_BASE_URL } from "@/config"

import { useCurrentUser } from "@/use/use-current-user"

const route = useRoute()
const boulderId = Number(route.params.id)

const imageUrl = computed(() => `${API_BASE_URL}/api/boulders/${boulderId}/image`)
const { currentUser, login } = useCurrentUser()

const boulder = ref<Boulder | null>(null)
const sends = ref<Send[]>([])
const isLoading = ref(true)
const sendsLoading = ref(true)
const error = ref<string | null>(null)

const detailMapContainer = ref<HTMLElement | null>(null)
let detailMap: L.Map | null = null

const showLogSendDialog = ref(false)
const sendSubmitting = ref(false)
const newSend = ref({ sendType: 2, rating: 0 })

const showLoginDialog = ref(false)
const loginUsername = ref("")
const loginLoading = ref(false)
const loginError = ref("")

function onLogSendClick() {
  if (currentUser.value) {
    showLogSendDialog.value = true
  } else {
    loginUsername.value = ""
    loginError.value = ""
    showLoginDialog.value = true
  }
}

async function handleLogin() {
  const trimmed = loginUsername.value.trim()
  if (!trimmed) return

  loginLoading.value = true
  loginError.value = ""

  try {
    await login(trimmed)
    showLoginDialog.value = false
    showLogSendDialog.value = true
  } catch (e) {
    loginError.value = "Failed to sign in. Please try again."
    console.error(e)
  } finally {
    loginLoading.value = false
  }
}

async function submitSend() {
  if (!currentUser.value) return

  sendSubmitting.value = true
  try {
    await sendsApi.create({
      boulderID: boulderId,
      userID: currentUser.value.id,
      sendType: newSend.value.sendType,
      rating: newSend.value.rating || null,
    })
    sends.value = await sendsApi.list({ boulderID: boulderId })
    showLogSendDialog.value = false
    newSend.value = { sendType: 2, rating: 0 }
  } catch (e) {
    console.error("Failed to log send:", e)
  } finally {
    sendSubmitting.value = false
  }
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
}

function parseCoords(coords: string): [number, number] | null {
  const match = coords.match(/^(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$/)
  if (!match) return null
  const lat = parseFloat(match[1])
  const lng = parseFloat(match[2])
  if (lat < -90 || lat > 90 || lng < -180 || lng > 180) return null
  return [lat, lng]
}

function initDetailMap() {
  if (!detailMapContainer.value || !boulder.value?.coordinates) return

  const parsed = parseCoords(boulder.value.coordinates)
  if (!parsed) return

  delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  })

  detailMap = L.map(detailMapContainer.value).setView(parsed, 14)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(detailMap)

  L.marker(parsed).addTo(detailMap)
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

  await nextTick()
  initDetailMap()

  try {
    sends.value = await sendsApi.list({ boulderID: boulderId })
  } catch (e) {
    console.error("Failed to load sends:", e)
  } finally {
    sendsLoading.value = false
  }
})

onBeforeUnmount(() => {
  if (detailMap) {
    detailMap.remove()
    detailMap = null
  }
})
</script>
