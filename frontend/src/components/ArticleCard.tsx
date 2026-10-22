import { Link } from 'react-router'
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
            <Link
                to={`/articles/${article.id}`}
                className="group block rounded-sm focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#FE413C]"
            >
                <article>
                    <time className="mb-2 block text-xs text-stone-500" dateTime={article.created_at}>
                        {new Intl.DateTimeFormat('en', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                        }).format(new Date(article.created_at))}
                    </time>
                    <h3 className="font-serif text-xl font-medium leading-snug transition-colors group-hover:text-[#FE413C] sm:text-2xl">
                        {article.title}
                    </h3>
                    <p className="mt-3 max-w-2xl text-sm text-stone-600 sm:text-base">
                        {excerpt}
                        {hasMoreWords && '…'}
                    </p>
                    <span className="mt-4 inline-block text-sm font-medium text-[#FE413C]">
                        Read article <span aria-hidden="true">→</span>
                    </span>
                </article>
            </Link>
        </li>
    )
}

export default ArticleCard
