import { reactive, toRefs, watch } from "vue"

import regionsApi, { type Region } from "@/api/regions-api"

export { type Region }

export function useRegions({ skipWatchIf = () => false }: { skipWatchIf?: () => boolean } = {}) {
  const state = reactive<{
    regions: Region[]
    isLoading: boolean
    isErrored: boolean
  }>({
    regions: [],
    isLoading: false,
    isErrored: false,
  })

  async function fetch(): Promise<Region[]> {
    state.isLoading = true
    try {
      const regions = await regionsApi.list()
      state.isErrored = false
      state.regions = regions
      return regions
    } catch (error) {
      console.error("Failed to fetch regions:", error)
      state.isErrored = true
      throw error
    } finally {
      state.isLoading = false
    }
  }

  watch(
    () => [skipWatchIf()],
    async ([skip]) => {
      if (skip) return

      await fetch()
    },
    { deep: true, immediate: true }
  )

  return {
    ...toRefs(state),
    fetch,
    refresh: fetch,
  }
}

export default useRegions
