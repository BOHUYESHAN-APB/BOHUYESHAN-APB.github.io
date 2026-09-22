import type { CardListData, Config, IntegrationUserConfig, ThemeUserConfig } from 'astro-pure/types'

export const theme: ThemeUserConfig = {
  // [Basic]
  /** Title for your website. Will be used in metadata and as browser tab title. */
  title: 'BoHuYeShan',
  /** Will be used in index page & copyright declaration */
  author: 'BoHuYeShan',
  /** Description metadata for your website. Can be used in page metadata. */
  description: '生物技术的底子，生信与 AI 是杠杆不是退路：生信工程、蛋白质语言模型、Agent 工作流，以及这个时代生物人手里的牌。只留干货，不做装饰。',
  /** The default favicon for your site which should be a path to an image in the `public/` directory. */
  favicon: '/favicon/favicon.ico',
  /** The default social card image for your site which should be a path to an image in the `public/` directory. */
  socialCard: '/images/social-card.png',
  /** Specify the default language for this site. */
  locale: {
    lang: 'zh-CN',
    attrs: 'zh_CN',
    // Date locale
    dateLocale: 'zh-CN',
    dateOptions: {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    }
  },
  /** Set a logo image to show in the homepage. */
  logo: {
    src: '/src/assets/avatar.jpg',
    alt: 'BoHuYeShan'
  },

  titleDelimiter: '•',
  prerender: true, // pagefind search is not supported with prerendering disabled
  npmCDN: 'https://cdn.jsdelivr.net/npm',

  // Still in test
  head: [
    { tag: 'link', attrs: { rel: 'llms', href: '/llms.txt' }, content: '' },
    { tag: 'meta', attrs: { name: 'llms-txt', content: '/llms.txt' }, content: '' },
    /* Telegram channel */
    // {
    //   tag: 'meta',
    //   attrs: { name: 'telegram:channel', content: '@cworld0_cn' },
    //   content: ''
    // }
  ],
  customCss: [],

  /** Configure the header of your site. */
  header: {
    menu: [
      { title: '博客', link: '/blog/' },
      { title: '归档', link: '/archives/' },
      { title: '摄影', link: '/photos/' },
      { title: '搜索', link: '/search/' },
      { title: '关于', link: '/about/' },
      { title: '支持', link: '/support/' }
    ]
  },

  /** Configure the footer of your site. */
  footer: {
    // Year format
    year: `© ${new Date().getFullYear()}`,
    links: [],
    /** Enable displaying a “Astro & Pure theme powered” link in your site’s footer. */
    credits: true,
    /** Optional details about the social media accounts for this site. */
    social: [
      { icon: 'github', label: 'GitHub', href: 'https://github.com/BOHUYESHAN-APB' },
      { icon: 'rss', label: 'RSS', href: '/rss.xml' }
    ]
  },

  // [Content]
  content: {
    /** External links configuration */
    externalLinks: {
      content: ' ↗',
      /** Properties for the external links element */
      properties: { style: 'user-select:none' }
    },
    /** Blog page size for pagination (optional) */
    blogPageSize: 8,
    /** Share buttons to show */
    // Schema only accepts weibo/x/bluesky; actual buttons come from
    // src/components/ShareButtons.astro (wechat QR + weibo + qq).
    share: ['weibo']
    /** Enable image captions (default false) */
    // imageCaption: true
  }
}

/**
 * 给予支持（/support 页与文章底部入口共用）。
 * 渠道留空即不渲染——没有空位。收款码图片放到 public/img/sponsor/ 后填根路径。
 */
export const sponsor = {
  /** 微信收款码图片，如 '/img/sponsor/wechat.png' */
  wechatQr: '',
  /** 支付宝收款码图片，如 '/img/sponsor/alipay.png' */
  alipayQr: '',
  /** 爱发电主页（国内） */
  afdian: 'https://afdian.com/a/bhys_afd',
  /** Buy Me a Coffee 主页（国际） */
  buyMeACoffee: '',
  /** GitHub Sponsors 主页（国际） */
  githubSponsors: ''
}

export const integ: IntegrationUserConfig = {
  // [Links]
  // https://astro-pure.js.org/docs/integrations/links
  links: {
    // Friend logbook
    logbook: [
      { date: '2025-03-16', content: 'Is there a leakage?' },
      { date: '2025-03-16', content: 'A leakage of what?' },
      { date: '2025-03-16', content: 'I have a full seat of water, like, full of water!' },
      { date: '2025-03-16', content: 'Must be the water.' },
      { date: '2025-03-16', content: "Let's add that to the words of wisdom." }
    ],
    // Yourself link info
    applyTip: [
      { name: 'Name', val: theme.title },
      { name: 'Desc', val: theme.description || 'Null' },
      { name: 'Link', val: 'https://astro-pure.js.org/' },
      { name: 'Avatar', val: 'https://astro-pure.js.org/favicon/favicon.ico' }
    ],
    // Cache avatars in `public/avatars/` to improve user experience.
    cacheAvatar: false
  },
  // [Search]
  pagefind: true,
  // Add a random quote to the footer (default on homepage footer)
  // See: https://astro-pure.js.org/docs/integrations/advanced#web-content-render
  // [Quote]
  quote: {
    // - Hitokoto（一言）：国内可达
    // https://developer.hitokoto.cn/sentence/
    server: 'https://v1.hitokoto.cn/?c=i&max_length=60',
    target: `(data) => (data.hitokoto || 'Error')`
  },
  // [Typography]
  // https://unocss.dev/presets/typography
  typography: {
    class: 'prose text-base',
    // The style of blockquote font `normal` / `italic` (default to italic in typography)
    blockquoteStyle: 'italic',
    // The style of inline code block `code` / `modern` (default to code in typography)
    inlineCodeBlockStyle: 'modern'
  },
  // [Lightbox]
  // A lightbox library that can add zoom effect
  // https://astro-pure.js.org/docs/integrations/others#medium-zoom
  mediumZoom: {
    enable: true, // disable it will not load the whole library
    selector: '.prose .zoomable',
    options: {
      className: 'zoomable'
    }
  },
  // Comment system
  waline: {
    enable: false,
    server: '',
    showMeta: false,
    emoji: [],
    additionalConfigs: {}
  }
}

export const terms: CardListData = {
  title: 'Terms content',
  list: [
    {
      title: 'Privacy Policy',
      link: '/terms/privacy-policy/'
    },
    {
      title: 'Terms and Conditions',
      link: '/terms/terms-and-conditions/'
    },
    {
      title: 'Copyright',
      link: '/terms/copyright/'
    },
    {
      title: 'Disclaimer',
      link: '/terms/disclaimer/'
    }
  ]
}

const config = { ...theme, integ } as Config
export default config
