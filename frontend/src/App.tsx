import { useEffect, useState } from 'react'
import './App.css'

type Article = {
    id: number
    title: string
    content: string
    author_id: number
    created_at: string
}

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
        );
    }

    if (error) {
        return (
            <main>
                <h1>Personal Blog</h1>
                <p>{error}</p>
            </main>
        );
    }

    return (
        <main>
            <h1>Personal Blog</h1>

            {articles.length === 0 ? (
                <p>No articles published yet.</p>
            ) : (
                <ul>
                    {articles.map((article) => (
                        <li key={article.id}>
                            <h2>{article.title}</h2>
                            <p>{article.content}</p>
                            <time dateTime={article.created_at}>
                                {new Date(article.created_at).toLocaleDateString('pt-BR')}
                            </time>
                        </li>
                    ))}
                </ul>
            )}
        </main>
    );
}

export default App
