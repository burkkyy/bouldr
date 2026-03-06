import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"
// _TODO_ add import guard for user "auth"

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("@/layouts/BlankLayout.vue"),
    children: [
      // {
      //   path: "/",
      //   name: "SplashPage",
      //   component: () => import("@/pages/SplashPage.vue"),
      //   meta: { requiresAuth: false },
      // },
      {
        path: "/sign-in",
        name: "SignInPage",
        component: () => import("@/pages/SignInPage.vue"),
        meta: { requiresAuth: false },
      },
      // {
      //   path: "/:pathMatch(.*)*",
      //   name: "NotFoundPage",
      //   component: () => import("@/pages/NotFoundPage.vue"),
      // },
    ],
  },
  // {
  //   path: "/",
  //   component: () => import("@/layouts/DefaultLayout.vue"),
  //   children: [
  //     {
  //       path: "/dashboard",
  //       name: "DashboardPage",
  //       component: () => import("@/pages/DashboardPage.vue"),
  //     },
  //     {
  //       path: "/status",
  //       name: "StatusPage",
  //       component: () => import("@/pages/StatusPage.vue"),
  //       meta: { requiresAuth: false },
  //     },
  //   ],
  // },
  // {
  //   path: "/administration",
  //   component: () => import("@/layouts/DefaultLayout.vue"),
  //   meta: { requiresAuth: true },
  //   children: [
  //     {
  //       path: "",
  //       name: "administration/DashboardPage",
  //       component: () =>
  //         import("@/pages/administration/AdministrationPage.vue"),
  //     },
  //   ],
  // },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Completely not nessessary?
// router.beforeEach(async (to) => {
//   if (to.meta.requiresAuth === false) return true;
//   // TODO: consider whether I should redirect to /sign-in instead of the auth0 login page?

//   const isAuthenticated = await authGuard(to);

//   if (isAuthenticated) return true;

//   // TODO: consider loading user in route guard?
//   // check if current user exists
//   // attempt to load current user, unless it's already been loaded?
//   // if current user does not exist, attempt to create a new user
//   // if current user still does exist, throw some kind of error?
//   // if meta.requiresRoleAdmin (or whatever) does not match or exceed current user role
//   // return false

//   return false;
// });

export default router
