import { createApp } from "vue"

// Plugins
import vuetify from "@/plugins/vuetify-plugin"
import vueI18nPlugin from "@/plugins/vue-i18n-plugin"

import VueScrollTo from "vue-scrollto"
import { PerfectScrollbarPlugin } from "vue3-perfect-scrollbar"
import router from "@/router"

import App from "@/App.vue"

const app = createApp(App)
app.use(router).use(vuetify).use(vueI18nPlugin)

app.use(PerfectScrollbarPlugin)

app.mount("#app")

app.use(VueScrollTo, {
  duration: 1000,
  easing: "ease",
})
