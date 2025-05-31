import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { TrendingUp, TrendingDown, Clock, ExternalLink } from 'lucide-react';
import type { NewsArticle } from '@/pages/Index';

interface NewsCardProps {
  article: NewsArticle;
}

const NewsCard = ({ article }: NewsCardProps) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return <TrendingUp className="h-4 w-4 text-green-600" />;
      case 'negative':
        return <TrendingDown className="h-4 w-4 text-red-600" />;
      default:
        return <div className="h-4 w-4 rounded-full bg-gray-400" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'negative':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const sectors = article.tags?.sectors ?? [];
  const stocks = article.tags?.stocks ?? [];

  return (
    <Card className="h-full flex flex-col hover:shadow-lg transition-shadow duration-200 border border-gray-200">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-lg leading-tight line-clamp-3">{article.title}</h3>
        </div>
        <div className="flex items-center text-sm text-gray-600 gap-2">
          <Clock className="h-4 w-4" />
          <span>{formatDate(article.publishedAt)}</span>
          <span className="font-medium">{article.source}</span>
        </div>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col">
        <p className="text-gray-700 text-sm mb-4 line-clamp-3 flex-1">
          {article.summary}
        </p>

        {/* Tags Section */}
        <div className="space-y-3">
          {/* Sentiment & Impact */}
          <div className="flex gap-2">
            <Badge className={`text-xs ${getSentimentColor(article.tags.sentiment)}`}>
              {article.tags.sentiment.toUpperCase()}
            </Badge>
            <Badge className={`text-xs ${getImpactColor(article.tags.impact)}`}>
              {article.tags.impact.toUpperCase()} IMPACT
            </Badge>
          </div>

          {/* Sectors */}
          {sectors.length > 0 && (
            <div>
              <p className="text-xs font-medium text-gray-600 mb-1">SECTORS:</p>
              <div className="flex flex-wrap gap-1">
                {sectors.map((sector) => (
                  <Badge key={sector} variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200">
                    {sector}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Stocks */}
          {stocks.length > 0 && (
            <div>
              <p className="text-xs font-medium text-gray-600 mb-1">STOCKS:</p>
              <div className="flex flex-wrap gap-1">
                {stocks.map((stock) => (
                  <Badge key={stock} variant="outline" className="text-xs bg-green-50 text-green-700 border-green-200 font-mono">
                    {stock}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Price (if present) */}
          {'price' in article && (
            <div>
              <p className="text-xs font-medium text-gray-600 mb-1">PRICE:</p>
              <p className="text-sm text-gray-600">Rs{(article as any).price ? ` ${(article as any).price.toFixed(2)}` : ''}</p>
            </div>
          )}
        </div>

        {/* Read More Button */}
        <Button
          variant="ghost"
          size="sm"
          className="mt-4 w-full justify-between"
          onClick={() => window.open(article.url, '_blank')}
        >
          <span>Read Full Article</span>
          <ExternalLink className="h-4 w-4" />
        </Button>
      </CardContent>
    </Card>
  );
};

export default NewsCard;
