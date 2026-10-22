import { useEffect, useState } from 'react'
import { Link, Outlet, Route, Routes, useParams } from 'react-router'
import logo from './assets/logo.svg'
import ArticleCard from './components/ArticleCard'
import type { Article } from './types/article'

const API_URL = 'http://localhost:8000/api'

function formatDate(value: string) {
    return new Intl.DateTimeFormat('en', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    }).format(new Date(value))
}

function SiteLayout() {
    return (
        <div id="top" className="min-h-screen bg-[#f7f6f5] text-stone-900">
            <header className="mx-auto w-full max-w-3xl px-6 pt-6 sm:px-8">
                <div className="flex items-center justify-between rounded-2xl border border-stone-200 bg-white px-5 py-4 shadow-xs">
                    <Link to="/" aria-label="Pina home">
                        <img src={logo} alt="Pina" className="h-8 w-auto" />
                    </Link>
                    <nav aria-label="Main navigation" className="flex items-center gap-6 text-sm text-stone-600">
                        <a className="transition-colors hover:text-[#FE413C] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber-700" href="/#articles">
                            Articles
                        </a>
                        <a className="transition-colors hover:text-[#FE413C] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber-700" href="/#contact">
                            Contact
                        </a>
                    </nav>
                </div>
            </header>

            <Outlet />

            <footer className="border-t border-stone-200">
                <div className="mx-auto flex max-w-3xl flex-col gap-2 px-6 py-6 text-xs text-stone-500 sm:flex-row sm:items-center sm:justify-between sm:px-8">
                    <Link to="/" aria-label="Pina home">
                        <img src={logo} alt="Pina" className="h-6 w-auto" />
                    </Link>
                    <p>Personal blog · Built with curiosity.</p>
                </div>
            </footer>
        </div>
    )
}

function HomePage() {
    const [articles, setArticles] = useState<Article[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function loadArticles() {
            try {
                const response = await fetch(`${API_URL}/articles?limit=4`)

                if (!response.ok) {
                    throw new Error('Failed to load articles.')
                }

                const data: Article[] = await response.json()
                setArticles(data)
            } catch {
                setError('We couldn’t load the articles. Please try again later.')
            } finally {
                setIsLoading(false)
            }
        }

        loadArticles()
    }, [])

    const featuredArticle = articles[0]
    const featuredParagraph = featuredArticle?.content.trim().split(/\r?\n\s*\r?\n/)[0]
    const secondaryArticles = articles.slice(1)

    return (
        <main className="mx-auto w-full max-w-3xl px-6 sm:px-8">
            <section className="py-16 sm:py-24" aria-labelledby="page-heading">
                <p className="mb-2 text-xs font-semibold uppercase tracking-[0.22em] text-[#FE413C]">
                    Notes, ideas &amp; things I learn
                </p>
                <h1 id="page-heading" className="max-w-2xl font-serif text-4xl font-medium leading-tight tracking-tight sm:text-6xl">
                    A personal space for thoughts worth sharing.
                </h1>
                <p className="mt-6 text-base leading-7 text-stone-600 sm:text-lg">
                    Writing about software, learning, and the ideas I come across along the way.
                </p>
            </section>

            <section id="articles" className="scroll-mt-8 pb-20" aria-labelledby="articles-heading">
                <div className="mb-7 flex items-end justify-between border-b border-stone-300 pb-3">
                    <h2 id="articles-heading" className="font-serif text-lg font-medium">Latest writing</h2>
                    <span className="text-xs uppercase tracking-[0.16em] text-stone-500">Articles</span>
                </div>

                {isLoading && (
                    <p role="status" className="py-10 text-sm text-stone-600">Loading articles...</p>
                )}
                {error && (
                    <p role="alert" className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
                        {error}
                    </p>
                )}

                {!isLoading && !error && articles.length === 0 && (
                    <p className="rounded-lg border border-dashed border-stone-300 px-6 py-12 text-center text-stone-600">
                        No articles published yet. Check back soon.
                    </p>
                )}

                {!isLoading && !error && featuredArticle && (
                    <>
                        <Link
                            to={`/articles/${featuredArticle.id}`}
                            className="group block rounded-2xl focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#FE413C]"
                        >
                            <article className="rounded-2xl border border-stone-200 bg-white p-6 shadow-[0_8px_32px_rgba(41,37,36,0.04)] transition-shadow group-hover:shadow-[0_12px_38px_rgba(41,37,36,0.10)] sm:p-9">
                                <p className="mb-5 text-xs font-semibold uppercase tracking-[0.18em] text-[#FE413C]">
                                    Featured article
                                </p>
                                <h3 className="font-serif text-3xl font-medium leading-tight tracking-tight transition-colors sm:text-4xl">
                                    {featuredArticle.title}
                                </h3>
                                <time className="mt-2 block text-sm text-stone-500" dateTime={featuredArticle.created_at}>
                                    {formatDate(featuredArticle.created_at)}
                                </time>
                                <p className="mt-6 whitespace-pre-line text-base text-stone-700">
                                    {featuredParagraph}…
                                </p>
                                <span className="mt-5 inline-block text-sm font-medium text-[#FE413C]">
                                    Read article <span aria-hidden="true">→</span>
                                </span>
                            </article>
                        </Link>

                        <section className="mt-16" aria-labelledby="recent-articles-heading">
                            <div className="mb-2 flex items-end justify-between border-b border-stone-300 pb-3">
                                <h2 id="recent-articles-heading" className="font-serif text-lg font-medium">
                                    More articles
                                </h2>
                                <span className="text-xs text-stone-500">{secondaryArticles.length} more</span>
                            </div>
                            {secondaryArticles.length === 0 ? (
                                <p className="py-6 text-sm text-stone-600">More articles will appear here.</p>
                            ) : (
                                <ul className="mx-auto flex flex-col divide-y divide-stone-200">
                                    {secondaryArticles.map((article) => (
                                        <ArticleCard key={article.id} article={article} />
                                    ))}
                                </ul>
                            )}
                        </section>
                    </>
                )}
            </section>

            <section id="contact" className="scroll-mt-8 border-t border-stone-300 py-14" aria-labelledby="contact-heading">
                <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-[#FE413C]">Say hello</p>
                <h2 id="contact-heading" className="font-serif text-3xl font-medium tracking-tight">Let’s keep in touch.</h2>
                <p className="mt-4 max-w-lg text-stone-600">
                    Thanks for reading. I’m always glad to connect with people who enjoy learning and building things.
                </p>
                <p className="mt-5 text-sm text-stone-500">Contact links coming soon.</p>
            </section>
        </main>
    )
}

function ArticlePage() {
    const { articleId } = useParams()
    const [article, setArticle] = useState<Article | null>(null)
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function loadArticle() {
            if (!articleId || !/^\d+$/.test(articleId)) {
                setError('This article could not be found.')
                setIsLoading(false)
                return
            }

            try {
                const response = await fetch(`${API_URL}/articles/${articleId}`)

                if (response.status === 404) {
                    setError('This article could not be found.')
                    return
                }
                if (!response.ok) {
                    throw new Error('Failed to load article.')
                }

                const data: Article = await response.json()
                setArticle(data)
            } catch {
                setError('We couldn’t load this article. Please try again later.')
            } finally {
                setIsLoading(false)
            }
        }

        setIsLoading(true)
        setError(null)
        setArticle(null)
        loadArticle()
    }, [articleId])

    return (
        <main className="mx-auto min-h-[70vh] w-full max-w-3xl px-6 py-12 sm:px-8 sm:py-16">
            <a href="/#articles" className="text-sm font-medium text-[#FE413C] hover:underline">
                <span aria-hidden="true">←</span> Back to articles
            </a>

            {isLoading && <p role="status" className="py-16 text-sm text-stone-600">Loading article...</p>}
            {error && (
                <div role="alert" className="py-16">
                    <h1 className="font-serif text-3xl font-medium">{error}</h1>
                    <p className="mt-4 text-stone-600">The article may have been removed, or there may be a connection problem.</p>
                </div>
            )}
            {!isLoading && !error && article && (
                <article className="py-12">
                    <p className="mb-2 text-xs font-semibold uppercase tracking-[0.18em] text-[#FE413C]">Article</p>
                    <h1 className="font-serif text-4xl font-medium leading-tight tracking-tight sm:text-5xl">
                        {article.title}
                    </h1>
                    <time className="mt-4 block text-sm text-stone-500" dateTime={article.created_at}>
                        {formatDate(article.created_at)}
                    </time>
                    <div className="mt-10 border-t border-stone-200 pt-8">
                        <p className="whitespace-pre-line text-base text-stone-700">
                            {article.content}
                        </p>
                    </div>
                </article>
            )}
        </main>
    )
}

function NotFoundPage() {
    return (
        <main className="mx-auto min-h-[70vh] w-full max-w-3xl px-6 py-16 sm:px-8">
            <h1 className="font-serif text-3xl font-medium">Page not found</h1>
            <p className="mt-3 text-stone-600">The page you’re looking for doesn’t exist.</p>
            <Link to="/" className="mt-6 inline-block text-sm font-medium text-[#FE413C] hover:underline">
                Return to home
            </Link>
        </main>
    )
}

function App() {
    return (
        <Routes>
            <Route element={<SiteLayout />}>
                <Route path="/" element={<HomePage />} />
                <Route path="/articles/:articleId" element={<ArticlePage />} />
                <Route path="*" element={<NotFoundPage />} />
            </Route>
        </Routes>
    )
}

export default App
