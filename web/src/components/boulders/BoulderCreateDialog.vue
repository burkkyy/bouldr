<template>
  <v-dialog
    v-model="showDialog"
    max-width="600"
    persistent
  >
    <v-card>
      <v-card-title>Create Boulder</v-card-title>
      <v-card-text>
        <v-form
          ref="formRef"
          @submit.prevent="validateAndCreate"
        >
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="boulder.name"
                label="Name"
                :rules="[required]"
                class="mb-2"
              />
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="boulder.grade"
                :items="gradeOptions"
                item-title="label"
                item-value="value"
                label="Grade"
                :rules="[required]"
                class="mb-2"
              />
            </v-col>
            <v-col cols="12">
              <v-combobox
                v-model="selectedRegion"
                :items="regionAutocompleteItems"
                label="Region"
                clearable
                class="mb-2"
                hint="Select an existing region or type a new one"
                persistent-hint
                :rules="[required]"
              />
              <v-select
                v-if="isNewRegion"
                v-model="newRegionType"
                :items="regionTypeOptions"
                label="New region type"
                :rules="[required]"
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
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="boulder.description"
                label="Description"
                rows="3"
                class="mb-2"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="boulder.coordinates"
                label="Coordinates"
                placeholder="e.g. 49.123, -123.456"
                :rules="[required]"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col
              cols="12"
              md="6"
            >
              <v-label class="mb-2">Profile Image</v-label>
              <v-file-input
                v-model="imageFile"
                accept="image/*"
                prepend-inner-icon="mdi-camera"
                label="Upload Image"
                hide-details="auto"
                clearable
                @change="handleImageUpload"
              />
              <div
                v-if="boulder.image"
                class="mt-4 d-flex justify-center"
              >
                <v-img
                  :src="boulder.image"
                  max-width="200"
                  max-height="200"
                  class="rounded elevation-2"
                  cover
                />
              </div>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          variant="text"
          text="Cancel"
          @click="close"
        />
        <v-btn
          color="primary"
          variant="flat"
          :loading="isCreating"
          text="Create"
          @click="validateAndCreate"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue"
import { VForm } from "vuetify/components"

import bouldersApi, { type Boulder } from "@/api/boulders-api"
import regionsApi from "@/api/regions-api"
import { required } from "@/utils/validators"
import { resizeToStandard } from "@/utils/image-resizer"

import useSnack from "@/use/use-snack"
import { useCurrentUser } from "@/use/use-current-user"
import useRegions from "@/use/use-regions"
import { isNil } from "lodash"

const showDialog = ref(false)

const { currentUser } = useCurrentUser()

const COORD_REGEX =
  /^-?(?:[1-8]?\d(?:\.\d+)?|90(?:\.0+)?),\s*-?(?:1[0-7]\d(?:\.\d+)?|180(?:\.0+)?|\d{1,2}(?:\.\d+)?)$/

const { regions } = useRegions()

const isCreating = ref(false)
const selectedRegion = ref<{ title: string; value: number } | string | null>(null)
const newRegionType = ref<string | null>(null)
const newRegionParentId = ref<number | null>(null)

const emit = defineEmits<{ created: [boulder: Boulder] }>()

const imageFile = ref<File[] | File | null>(null)

const boulder = ref<Partial<Boulder>>({
  authorID: currentUser.value?.id ?? 1,
})

const grades = {
  V0: 0,
  V1: 1,
  V2: 2,
  V3: 3,
  V4: 4,
  V5: 5,
  V6: 6,
  V7: 7,
  V8: 8,
  V9: 9,
  V10: 10,
  V11: 11,
  V12: 12,
  V13: 13,
  V14: 14,
  V15: 15,
  V16: 16,
  V17: 17,
}

const gradeOptions = Object.entries(grades).map(([key, val]) => ({
  label: key,
  value: val,
}))

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

const formRef = ref<InstanceType<typeof VForm> | null>(null)
const snack = useSnack()

async function handleImageUpload() {
  const file = Array.isArray(imageFile.value) ? imageFile.value[0] : imageFile.value

  if (isNil(file) || !(file instanceof File)) {
    boulder.value.image = null
    snack.error("Bad file upload")
    return
  }

  try {
    boulder.value.image = await resizeToStandard(file)
  } catch (error) {
    console.error("Error resizing profile image:", error)
    snack.error("Failed to process profile image")
  }
}

async function validateAndCreate() {
  if (formRef.value === null) return

  const { valid } = await formRef.value.validate()

  if (!valid) return

  const coords = boulder.value.coordinates?.trim()
  if (coords && !COORD_REGEX.test(coords)) return

  isCreating.value = true

  try {
    // _TODO_ refactor
    let regionId: number | null = null
    if (typeof selectedRegion.value === "string" && selectedRegion.value.trim()) {
      if (!newRegionType.value) {
        throw new Error("Please select a type for the new region.")
      }
      const newRegion = await regionsApi.create({
        type: newRegionType.value,
        name: selectedRegion.value.trim(),
        parentId: newRegionParentId.value,
      })
      regionId = newRegion.id
    } else if (selectedRegion.value && typeof selectedRegion.value === "object") {
      regionId = selectedRegion.value.value
    }

    const newBoulder = await bouldersApi.create({
      ...boulder.value,
      regionID: regionId,
      coordinates: coords || null,
    })
    emit("created", newBoulder)
    close()
  } catch (e) {
    snack.error("Failed to create boulder.")
    console.error(e)
  } finally {
    isCreating.value = false
  }
}

function show() {
  showDialog.value = true
}

function close() {
  boulder.value = {}
  showDialog.value = false
}

defineExpose({ show, close })
</script>
