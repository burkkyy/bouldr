<template>
  <v-dialog
    v-model="showDialog"
    max-width="600"
    persistent
  >
    <v-card>
      <v-card-title>{{ isEditMode ? "Edit Boulder" : "Create Boulder" }}</v-card-title>
      <v-card-text>
        <v-form
          ref="formRef"
          @submit.prevent="validateAndSubmit"
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
                :label="isEditMode ? 'Upload New Image' : 'Upload Image'"
                hide-details="auto"
                clearable
                @change="handleImageUpload"
              />
              <div
                v-if="boulder.image || existingImageUrl"
                class="mt-4 d-flex justify-center"
              >
                <v-img
                  :src="boulder.image || existingImageUrl || ''"
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
          :loading="isSubmitting"
          :text="isEditMode ? 'Save' : 'Create'"
          @click="validateAndSubmit"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue"
import { VForm } from "vuetify/components"
import { isNil } from "lodash"

import bouldersApi, { type Boulder } from "@/api/boulders-api"
import regionsApi from "@/api/regions-api"
import { required } from "@/utils/validators"
import { resizeToStandard } from "@/utils/image-resizer"
import { API_BASE_URL } from "@/config"

import useSnack from "@/use/use-snack"
import { useCurrentUser } from "@/use/use-current-user"
import useRegions from "@/use/use-regions"

const showDialog = ref(false)
const isEditMode = ref(false)
let editingBoulderId: number | null = null

const { currentUser } = useCurrentUser()

const COORD_REGEX =
  /^-?(?:[1-8]?\d(?:\.\d+)?|90(?:\.0+)?),\s*-?(?:1[0-7]\d(?:\.\d+)?|180(?:\.0+)?|\d{1,2}(?:\.\d+)?)$/

const { regions } = useRegions()

const isSubmitting = ref(false)
const selectedRegion = ref<{ title: string; value: number } | string | null>(null)
const newRegionType = ref<string | null>(null)
const newRegionParentId = ref<number | null>(null)
const existingImageUrl = ref<string | null>(null)

const emit = defineEmits<{
  created: [boulder: Boulder]
  updated: [boulder: Boulder]
}>()

const imageFile = ref<File[] | File | null>(null)

const boulder = ref<Partial<Boulder>>({
  authorId: currentUser.value?.id ?? 1,
})

const grades = {
  V0: 0, V1: 1, V2: 2, V3: 3, V4: 4, V5: 5, V6: 6, V7: 7, V8: 8,
  V9: 9, V10: 10, V11: 11, V12: 12, V13: 13, V14: 14, V15: 15, V16: 16, V17: 17,
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

async function validateAndSubmit() {
  if (formRef.value === null) return

  const { valid } = await formRef.value.validate()
  if (!valid) return

  const coords = boulder.value.coordinates?.trim()
  if (coords && !COORD_REGEX.test(coords)) return

  isSubmitting.value = true

  try {
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

    if (isEditMode.value && editingBoulderId !== null) {
      const attrs: Partial<Boulder> = {
        name: boulder.value.name,
        grade: boulder.value.grade,
        description: boulder.value.description || null,
        coordinates: coords || null,
        regionId: regionId,
      }
      if (boulder.value.image) {
        attrs.image = boulder.value.image
      }
      const updated = await bouldersApi.update(editingBoulderId, attrs)
      emit("updated", updated)
      snack.success("Boulder updated")
    } else {
      const newBoulder = await bouldersApi.create({
        ...boulder.value,
        regionId: regionId,
        coordinates: coords || null,
      })
      emit("created", newBoulder)
    }
    close()
  } catch (e) {
    snack.error(isEditMode.value ? "Failed to update boulder." : "Failed to create boulder.")
    console.error(e)
  } finally {
    isSubmitting.value = false
  }
}

function show() {
  isEditMode.value = false
  editingBoulderId = null
  existingImageUrl.value = null
  boulder.value = { authorId: currentUser.value?.id ?? 1 }
  selectedRegion.value = null
  newRegionType.value = null
  newRegionParentId.value = null
  imageFile.value = null
  showDialog.value = true
}

function showEdit(existing: Boulder) {
  isEditMode.value = true
  editingBoulderId = existing.id
  boulder.value = {
    name: existing.name,
    grade: existing.grade,
    description: existing.description || "",
    coordinates: existing.coordinates || "",
  }
  existingImageUrl.value = existing.image
    ? `${API_BASE_URL}/api/boulders/${existing.id}/image`
    : null
  imageFile.value = null

  // Set region if it exists
  if (existing.regionId) {
    const region = regions.value.find((r) => r.id === existing.regionId)
    if (region) {
      selectedRegion.value = { title: `${region.name} (${region.type})`, value: region.id }
    }
  } else {
    selectedRegion.value = null
  }
  newRegionType.value = null
  newRegionParentId.value = null

  showDialog.value = true
}

function showWithPrefill(prefill: Partial<Boulder>) {
  isEditMode.value = false
  editingBoulderId = null
  existingImageUrl.value = null
  boulder.value = {
    authorId: currentUser.value?.id ?? 1,
    ...prefill,
  }
  // Try to match region by name
  if (prefill.regionId) {
    const region = regions.value.find((r) => r.id === prefill.regionId)
    if (region) {
      selectedRegion.value = { title: `${region.name} (${region.type})`, value: region.id }
    }
  } else {
    selectedRegion.value = null
  }
  newRegionType.value = null
  newRegionParentId.value = null
  imageFile.value = null
  showDialog.value = true
}

function close() {
  boulder.value = {}
  existingImageUrl.value = null
  showDialog.value = false
  isEditMode.value = false
  editingBoulderId = null
}

defineExpose({ show, showEdit, showWithPrefill, close })
</script>
