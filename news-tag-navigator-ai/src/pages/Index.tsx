import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, Filter, TrendingUp, TrendingDown } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { toast } from '@/hooks/use-toast';
import NewsCard from '@/components/NewsCard';
import FilterSidebar from '@/components/FilterSidebar';
import StatsOverview from '@/components/StatsOverview';
import SignalsSection from '@/components/SignalsSection';
import type { Signal } from '@/components/SignalCard';

export interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  content: string;
  publishedAt: string;
  source: string;
  url: string;
  tags: {
    sectors: string[];
    stocks: string[];
    sentiment: 'positive' | 'negative' | 'neutral';
    impact: 'high' | 'medium' | 'low';
  };
}

const API_BASE = 'http://localhost:8001/api';

const fetchSignals = async (): Promise<Signal[]> => {
  const res = await fetch(`${API_BASE}/signals/`);
  if (!res.ok) throw new Error('Failed to fetch signals');
  const data = await res.json();
  return Array.isArray(data.results) ? data.results : [];
};

const fetchNewsData = async (): Promise<NewsArticle[]> => {
  const res = await fetch(`${API_BASE}/analyzed-news/`);
  if (!res.ok) throw new Error('Failed to fetch news');
  const data = await res.json();
  return Array.isArray(data.results) ? data.results : [];
};

const Index = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSectors, setSelectedSectors] = useState<string[]>([]);
  const [selectedStocks, setSelectedStocks] = useState<string[]>([]);
  const [selectedSentiment, setSelectedSentiment] = useState<string>('');
  const [showFilters, setShowFilters] = useState(false);

  const { data: signals = [], isLoading: signalsLoading } = useQuery({
    queryKey: ['signals'],
    queryFn: fetchSignals,
    refetchInterval: 60000,
  });

  const { data: newsArticles = [], isLoading: newsLoading } = useQuery({
    queryKey: ['news'],
    queryFn: fetchNewsData,
    refetchInterval: 60000,
  });

  const filteredArticles = newsArticles.filter((article) => {
    const matchesSearch = searchQuery === '' || 
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.summary.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSectors = selectedSectors.length === 0 || 
      selectedSectors.some(sector => (article.tags.sectors ?? []).includes(sector));
    const matchesStocks = selectedStocks.length === 0 || 
      selectedStocks.some(stock => (article.tags.stocks ?? []).includes(stock));
    const matchesSentiment = selectedSentiment === '' || 
      article.tags.sentiment === selectedSentiment;
    return matchesSearch && matchesSectors && matchesStocks && matchesSentiment;
  });

  const allSectors = Array.from(new Set(newsArticles.flatMap(article => article.tags.sectors).filter(Boolean))) as string[];
  const allStocks = Array.from(new Set(newsArticles.flatMap(article => article.tags.stocks).filter(Boolean))) as string[];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <TrendingUp className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">AI Market News</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
                className="hidden md:flex items-center space-x-2"
              >
                <Filter className="h-4 w-4" />
                <span>Filters</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <StatsOverview articles={filteredArticles} />
        {/* Signals Section */}
        <SignalsSection signals={signals} />
        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <Input
              placeholder="Search news articles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 py-3 text-lg"
            />
          </div>
        </div>
        {/* Sidebar Filters */}
        {showFilters && (
          <div className="w-80 hidden md:block">
            <FilterSidebar
              sectors={allSectors}
              stocks={allStocks}
              selectedSectors={selectedSectors}
              selectedStocks={selectedStocks}
              selectedSentiment={selectedSentiment}
              onSectorsChange={setSelectedSectors}
              onStocksChange={setSelectedStocks}
              onSentimentChange={setSelectedSentiment}
            />
          </div>
        )}
        {/* News Articles */}
        <div className="flex-1">
          {newsLoading ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="bg-gray-200 rounded-lg h-64"></div>
                </div>
              ))}
            </div>
          ) : filteredArticles.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredArticles.map((article) => (
                <NewsCard key={article.id} article={article as any} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <TrendingDown className="h-16 w-16 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No articles found</h3>
              <p className="text-gray-600">Try adjusting your search or filter criteria.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Index;
