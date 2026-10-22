import { useEffect, useState } from 'react'
import ArticleCard from './components/ArticleCard'
import type { Article } from './types/article'

function App() {
    const [articles, setArticles] = useState<Article[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function loadArticles() {
            try {
                const response = await fetch('http://localhost:8000/api/articles?limit=4')

                if (!response.ok) {
                    throw new Error('Failed to load articles. Please try again later.')
                }

                const data: Article[] = await response.json()
                setArticles(data)
            } catch {
                setError('Failed to load articles. Please try again later.')
            } finally {
                setIsLoading(false)
            }
        }

        loadArticles()
    }, [])

    const featuredArticle = articles[0]
    const secondaryArticles = articles.slice(1)

    return (
        <div className="min-h-screen bg-stone-50 text-stone-900" id="top">
            <header className="mx-auto flex w-full max-w-2xl items-center justify-between px-6 py-12">
                <a href="#top" aria-label="Pina home">Pina</a>
                <nav aria-label="Main navigation">
                    <a href="#articles">Articles</a>
                    <a href="#contact">Contact</a>
                </nav>
            </header>

            <main className="mx-auto w-full max-w-2xl px-6 py-12">
                <h1 className="text-3xl font-bold">Personal Blog</h1>

                <section id="articles" aria-labelledby="articles-heading">
                    <h2 id="articles-heading">Articles</h2>

                    {isLoading && <p>Loading articles...</p>}
                    {error && <p role="alert">{error}</p>}

                    {!isLoading && !error && articles.length === 0 && (
                        <p>No articles published yet.</p>
                    )}

                    {!isLoading && !error && featuredArticle && (
                        <>
                            <section aria-labelledby="featured-article-heading">
                                <h2 id="featured-article-heading">Featured article</h2>
                                <article>
                                    <h3>{featuredArticle.title}</h3>
                                    <time dateTime={featuredArticle.created_at}>
                                        {new Date(featuredArticle.created_at).toLocaleDateString('pt-BR')}
                                    </time>
                                    <p>{featuredArticle.content}</p>
                                </article>
                            </section>

                            <section aria-labelledby="recent-articles-heading">
                                <h2 id="recent-articles-heading">Recent articles</h2>
                                {secondaryArticles.length === 0 ? (
                                    <p>No other articles yet.</p>
                                ) : (
                                    <ul>
                                        {secondaryArticles.map((article) => (
                                            <ArticleCard key={article.id} article={article} />
                                        ))}
                                    </ul>
                                )}
                            </section>
                        </>
                    )}
                </section>
            </main>

            <footer className="mx-auto w-full max-w-2xl px-6 py-12" id="contact">
                <h2>Contact</h2>
            </footer>
        </div>
    )
}

export default App
