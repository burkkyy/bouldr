import { createApp } from "vue"

// Plugins
import vuetify from "@/plugins/vuetify-plugin"

import VueScrollTo from "vue-scrollto"
import { PerfectScrollbarPlugin } from "vue3-perfect-scrollbar"
import router from "@/router"

import App from "@/App.vue"

const app = createApp(App)
app.use(router).use(vuetify)

app.use(PerfectScrollbarPlugin)

app.mount("#app")

app.use(VueScrollTo, {
  duration: 1000,
  easing: "ease",
})
