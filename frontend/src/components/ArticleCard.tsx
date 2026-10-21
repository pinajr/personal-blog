import type { Article } from '../types/article'

type ArticleCardProps = {
    article: Article
}

function ArticleCard({ article }: ArticleCardProps) {
    return (
        <li>
            <h2>{article.title}</h2>
            <p>{article.content}</p>
            <time dateTime={article.created_at}>
                {new Date(article.created_at).toLocaleDateString('pt-BR')}
            </time>
        </li>
    )
}

export default ArticleCard