import { useEffect, useState } from 'react'
import ArticleCard from './components/ArticleCard'
import type { Article } from './types/article'
import './App.css'

function App() {
    const [articles, setArticles] = useState<Article[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function loadArticles() {
            try {
                const response = await fetch('http://localhost:8000/api/articles')

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

    if (isLoading) {
        return (
            <main>
                <h1>Personal Blog</h1>
                <p>Loading articles...</p>
            </main>
        )
    }

    if (error) {
        return (
            <main>
                <h1>Personal Blog</h1>
                <p>{error}</p>
            </main>
        )
    }

    return (
        <main>
            <h1>Personal Blog</h1>

            {articles.length === 0 ? (
                <p>No articles published yet.</p>
            ) : (
                <ul>
                    {articles.map((article) => (
                        <ArticleCard key={article.id} article={article} />
                    ))}
                </ul>
            )}
        </main>
    )
}

export default App
