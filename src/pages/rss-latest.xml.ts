import type { AstroGlobal } from 'astro'

import { createFeed } from './rss.xml'

/**
 * Feed for the GitHub profile card: the three newest posts, pinned posts excluded.
 * The pinned entry is written by hand above the generated block, so it must not repeat here.
 */
const GET = (context: AstroGlobal) => createFeed(context, { limit: 3, pinned: 'exclude' })

export { GET }
