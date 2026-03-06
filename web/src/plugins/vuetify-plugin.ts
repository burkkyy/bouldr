/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import "@mdi/font/css/materialdesignicons.css"
import "vuetify/styles"
import "@/assets/main.scss"

// Composables
import { createVuetify } from "vuetify"
import * as labs from "vuetify/labs/components"

import { THEME } from "@/theme/Theme"

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  components: {
    ...labs,
  },
  theme: {
    defaultTheme: "THEME",
    themes: {
      THEME,
    },
  },
  defaults: {
    VCard: {
      rounded: "md",
      variant: "flat",
    },
    VTextField: {
      variant: "outlined",
      density: "comfortable",
      color: "primary",
      autocomplete: "null",
      bgColor: "white",
      hideDetails: "auto",
      baseColor: "primary",
    },
    VTextarea: {
      variant: "outlined",
      density: "comfortable",
      color: "primary",
      bgColor: "white",
      hideDetails: "auto",
      baseColor: "primary",
    },
    VSelect: {
      variant: "outlined",
      density: "comfortable",
      color: "primary",
      bgColor: "white",
      hideDetails: "auto",
    },
    VAutocomplete: {
      variant: "outlined",
      density: "comfortable",
      color: "primary",
      bgColor: "white",
      hideDetails: "auto",
    },
    VCombobox: {
      variant: "outlined",
      density: "comfortable",
      color: "primary",
      bgColor: "white",
      hideDetails: "auto",
    },
    VFileInput: {
      variant: "outlined",
      density: "comfortable",
      color: "primary",
      bgColor: "white",
      hideDetails: "auto",
      prependInnerIcon: "mdi-paperclip",
      prependIcon: ""
    },
    VListItem: {
      minHeight: "45px",
    },
    VTooltip: {
      location: "top",
    },
    VSwitch: {
      color: "success",
      baseColor: "primary",
      density: "comfortable",
      hideDetails: "auto",
    },
    VBtn: { color: "primary", variant: "flat", style: "text-transform: none;" },
  },
})
