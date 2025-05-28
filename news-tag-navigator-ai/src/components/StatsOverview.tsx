
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, TrendingDown, BarChart, Newspaper } from 'lucide-react';
import type { NewsArticle } from '@/pages/Index';

interface StatsOverviewProps {
  articles: NewsArticle[];
}

const StatsOverview = ({ articles }: StatsOverviewProps) => {
  const totalArticles = articles.length;
  const positiveArticles = articles.filter(a => a.tags.sentiment === 'positive').length;
  const negativeArticles = articles.filter(a => a.tags.sentiment === 'negative').length;
  const neutralArticles = articles.filter(a => a.tags.sentiment === 'neutral').length;
  const highImpactArticles = articles.filter(a => a.tags.impact === 'high').length;

  const stats = [
    {
      title: 'Total Articles',
      value: totalArticles,
      icon: Newspaper,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Positive Sentiment',
      value: positiveArticles,
      icon: TrendingUp,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Negative Sentiment',
      value: negativeArticles,
      icon: TrendingDown,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      title: 'High Impact',
      value: highImpactArticles,
      icon: BarChart,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {stats.map((stat) => (
        <Card key={stat.title} className="border border-gray-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`p-3 rounded-full ${stat.bgColor}`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default StatsOverview;
