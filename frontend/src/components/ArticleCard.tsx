import type { Article } from '../types/article'

const MAX_WORDS = 23

type ArticleCardProps = {
    article: Article
}

function ArticleCard({ article }: ArticleCardProps) {
    const words = article.content.trim().split(/\s+/)
    const excerpt = words.slice(0, MAX_WORDS).join(' ')
    const hasMoreWords = words.length > MAX_WORDS

    return (
        <li className="py-6 sm:py-7">
            <article>
                <time className="mb-2 block text-xs text-stone-500" dateTime={article.created_at}>
                    {new Intl.DateTimeFormat('en', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                    }).format(new Date(article.created_at))}
                </time>
                <h3 className="font-serif text-xl font-medium leading-snug sm:text-2xl">
                    {article.title}
                </h3>
                <p className="mt-3 max-w-2xl text-sm text-stone-600 sm:text-base">
                    {excerpt}
                    {hasMoreWords && '…'}
                </p>

            </article>
        </li>
    )
}

export default ArticleCard
