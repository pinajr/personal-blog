import { useEffect, useState } from 'react'
import ArticleCard from './components/ArticleCard'
import type { Article } from './types/article'

function formatDate(value: string) {
    return new Intl.DateTimeFormat('en', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    }).format(new Date(value))
}

function App() {
    const [articles, setArticles] = useState<Article[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function loadArticles() {
            try {
                const response = await fetch('http://localhost:8000/api/articles?limit=4')

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
    const secondaryArticles = articles.slice(1)

    return (
        <div id="top" className="min-h-screen bg-[#f7f6f5] text-stone-900">
            <header className="border-b border-stone-200/80">
                <div className="mx-auto flex max-w-3xl items-center justify-between px-6 py-6 sm:px-8">
                    <a
                        href="#top"
                        aria-label="Pina home"
                        className="font-serif text-2xl font-semibold tracking-tight"
                    >
                        pina<span className="text-amber-700">.</span>
                    </a>
                    <nav aria-label="Main navigation" className="flex items-center gap-6 text-sm text-stone-600">
                        <a className="transition-colors hover:text-amber-800 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber-700" href="#articles">
                            Articles
                        </a>
                        <a className="transition-colors hover:text-amber-800 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber-700" href="#contact">
                            Contact
                        </a>
                    </nav>
                </div>
            </header>

            <main className="mx-auto w-full max-w-3xl px-6 sm:px-8">
                <section className="py-16 sm:py-24" aria-labelledby="page-heading">
                    <p className="mb-2 text-xs font-semibold uppercase tracking-[0.22em] text-amber-800">
                        Notes, ideas &amp; things I learn
                    </p>
                    <h1 id="page-heading" className="max-w-2xl font-serif text-4xl font-medium leading-tight tracking-tight sm:text-6xl">
                        A personal space for thoughts worth sharing.
                    </h1>
                    <p className="mt-6 max-w-xl text-base leading-7 text-stone-600 sm:text-lg">
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
                            <article className="rounded-2xl border border-stone-200 bg-white p-6 shadow-[0_8px_32px_rgba(41,37,36,0.04)] sm:p-9">
                                <p className="mb-5 text-xs font-semibold uppercase tracking-[0.18em] text-amber-800">
                                    Featured article
                                </p>
                                <h3 className="font-serif text-3xl font-medium leading-tight tracking-tight sm:text-4xl">
                                    {featuredArticle.title}
                                </h3>
                                <time className="mt-2 block text-sm text-stone-500" dateTime={featuredArticle.created_at}>
                                    {formatDate(featuredArticle.created_at)}
                                </time>
                                <p className="mt-6 whitespace-pre-line text-base text-stone-700">
                                    {featuredArticle.content}
                                </p>
                            </article>

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
                    <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-amber-800">Say hello</p>
                    <h2 id="contact-heading" className="font-serif text-3xl font-medium tracking-tight">Let’s keep in touch.</h2>
                    <p className="mt-4 max-w-lg text-stone-600">
                        Thanks for reading. I’m always glad to connect with people who enjoy learning and building things.
                    </p>
                    <p className="mt-5 text-sm text-stone-500">Contact links coming soon.</p>
                </section>
            </main>

            <footer className="border-t border-stone-200">
                <div className="mx-auto flex max-w-3xl flex-col gap-2 px-6 py-6 text-xs text-stone-500 sm:flex-row sm:items-center sm:justify-between sm:px-8">
                    <a href="#top" className="font-serif text-base font-semibold text-stone-800">pina.</a>
                    <p>Personal blog · Built with curiosity.</p>
                </div>
            </footer>
        </div>
    )
}

export default App
