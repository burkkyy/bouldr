export type WhereOptions<Model, Attributes extends keyof Model> = {
  [K in Attributes]?: Model[K] | Model[K][]
}

export type FiltersOptions<Options> = Partial<Options>

export type QueryOptions<WhereOptions, FiltersOptions> = Partial<{
  where: WhereOptions
  filters: FiltersOptions
  page: number
  perPage: number
}>

export const MAX_PER_PAGE = 1000
