import { defineCollection } from 'astro:content'
import { glob } from 'astro/loaders'
import { z } from 'astro/zod'

function removeDups(array: string[]) {
  if (!array.length) return array
  // Keep original casing (GWAS, AI for Science…) — only deduplicate
  return Array.from(new Set(array))
}

// Define blog collection
const blog = defineCollection({
  // Load Markdown and MDX files in the `src/content/blog/` directory.
  loader: glob({
    base: './src/content/blog',
    pattern: '**/*.{md,mdx}',
    // Preserve filename casing so URLs stay byte-identical to the
    // archived Hexo site (Agent/LLM/FASTQ… must not be slugified).
    generateId: ({ entry }) => entry.replace(/\.(md|mdx)$/, '').replace(/\/index$/, '')
  }),
  // Required
  schema: ({ image }) =>
    z.object({
      // Required
      title: z.string().max(120),
      description: z.string().max(200),
      publishDate: z.coerce.date(),
      // Optional
      updatedDate: z.coerce.date().optional(),
      heroImage: z
        .object({
          src: image(),
          alt: z.string().optional(),
          inferSize: z.boolean().optional(),
          width: z.number().optional(),
          height: z.number().optional(),

          color: z.string().optional()
        })
        .optional(),
      tags: z.array(z.string()).default([]).transform(removeDups),
      language: z.string().optional(),
      draft: z.boolean().default(false),
      // Special fields
      comment: z.boolean().default(false)
    })
})

// Define docs collection
const docs = defineCollection({
  loader: glob({
    base: './src/content/docs',
    pattern: '**/*.{md,mdx}',
    generateId: ({ entry }) => entry.replace(/\.(md|mdx)$/, '').replace(/\/index$/, '')
  }),
  schema: () =>
    z.object({
      title: z.string().max(60),
      description: z.string().max(160),
      publishDate: z.coerce.date().optional(),
      updatedDate: z.coerce.date().optional(),
      tags: z.array(z.string()).default([]).transform(removeDups),
      draft: z.boolean().default(false),
      // Special fields
      order: z.number().default(999)
    })
})

export const collections = { blog, docs }
