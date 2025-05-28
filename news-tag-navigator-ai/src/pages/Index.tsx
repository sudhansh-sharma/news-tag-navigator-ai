import { useState, useEffect } from 'react';
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

const Index = () => {
  const [apiEndpoint, setApiEndpoint] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSectors, setSelectedSectors] = useState<string[]>([]);
  const [selectedStocks, setSelectedStocks] = useState<string[]>([]);
  const [selectedSentiment, setSelectedSentiment] = useState<string>('');
  const [showFilters, setShowFilters] = useState(false);

  // Mock signals data
  const mockSignalsData: Signal[] = [
    {
      id: '1',
      type: 'buy',
      symbol: 'AAPL',
      price: 175.50,
      timestamp: '2024-01-15T10:30:00Z',
      confidence: 'high',
      reason: 'Strong earnings beat with positive guidance for Q1 2024'
    },
    {
      id: '2',
      type: 'sell',
      symbol: 'TSLA',
      price: 210.25,
      timestamp: '2024-01-15T09:45:00Z',
      confidence: 'medium',
      reason: 'Technical indicators showing overbought conditions'
    },
    {
      id: '3',
      type: 'entry',
      symbol: 'NVDA',
      price: 495.80,
      timestamp: '2024-01-15T08:15:00Z',
      confidence: 'high',
      reason: 'AI sector momentum with breakthrough in chip technology'
    }
  ];

  // Mock data for demonstration - replace with actual API call
  const mockNewsData: NewsArticle[] = [
    {
      id: '1',
      title: 'Apple Reports Record Q4 Earnings, Beats Wall Street Expectations',
      summary: 'Apple Inc. posted better-than-expected quarterly results driven by strong iPhone sales and services revenue growth.',
      content: 'Full article content here...',
      publishedAt: '2024-01-15T10:30:00Z',
      source: 'Financial Times',
      url: 'https://example.com/news/1',
      tags: {
        sectors: ['Technology', 'Consumer Electronics'],
        stocks: ['AAPL'],
        sentiment: 'positive',
        impact: 'high'
      }
    },
    {
      id: '2',
      title: 'Banking Sector Faces Regulatory Scrutiny Over Climate Risk',
      summary: 'Federal regulators are increasing oversight of major banks\' climate-related financial disclosures.',
      content: 'Full article content here...',
      publishedAt: '2024-01-15T09:15:00Z',
      source: 'Reuters',
      url: 'https://example.com/news/2',
      tags: {
        sectors: ['Banking', 'Financial Services'],
        stocks: ['JPM', 'BAC', 'WFC'],
        sentiment: 'negative',
        impact: 'medium'
      }
    },
    {
      id: '3',
      title: 'Tesla Announces New Gigafactory in Mexico, Stock Surges',
      summary: 'Electric vehicle maker Tesla unveiled plans for a new manufacturing facility in Mexico, boosting investor confidence.',
      content: 'Full article content here...',
      publishedAt: '2024-01-15T08:45:00Z',
      source: 'Bloomberg',
      url: 'https://example.com/news/3',
      tags: {
        sectors: ['Automotive', 'Clean Energy'],
        stocks: ['TSLA'],
        sentiment: 'positive',
        impact: 'high'
      }
    }
  ];

  const fetchNewsData = async (): Promise<NewsArticle[]> => {
    if (!apiEndpoint) {
      // Return mock data if no API endpoint is provided
      return mockNewsData;
    }

    try {
      const response = await fetch(apiEndpoint, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch news data');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching news:', error);
      toast({
        title: "Error",
        description: "Failed to fetch news data. Using demo data instead.",
        variant: "destructive",
      });
      return mockNewsData;
    }
  };

  const { data: newsArticles = [], isLoading, error } = useQuery({
    queryKey: ['news', apiEndpoint, selectedSectors, selectedStocks, selectedSentiment],
    queryFn: fetchNewsData,
    refetchInterval: 300000, // Refetch every 5 minutes
  });

  const filteredArticles = newsArticles.filter((article) => {
    const matchesSearch = searchQuery === '' || 
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.summary.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesSectors = selectedSectors.length === 0 || 
      selectedSectors.some(sector => article.tags.sectors.includes(sector));
    
    const matchesStocks = selectedStocks.length === 0 || 
      selectedStocks.some(stock => article.tags.stocks.includes(stock));
    
    const matchesSentiment = selectedSentiment === '' || 
      article.tags.sentiment === selectedSentiment;
    
    return matchesSearch && matchesSectors && matchesStocks && matchesSentiment;
  });

  const allSectors = Array.from(new Set(newsArticles.flatMap(article => article.tags.sectors)));
  const allStocks = Array.from(new Set(newsArticles.flatMap(article => article.tags.stocks)));

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
        {/* API Endpoint Input */}
        <Card className="mb-8">
          <CardHeader>
            <h2 className="text-lg font-semibold">API Configuration</h2>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              <Input
                placeholder="Enter your API endpoint URL"
                value={apiEndpoint}
                onChange={(e) => setApiEndpoint(e.target.value)}
                className="flex-1"
              />
              <Button onClick={() => window.location.reload()}>
                Connect
              </Button>
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Leave empty to view demo data. Your API should return an array of news articles with tags.
            </p>
          </CardContent>
        </Card>

        {/* Stats Overview */}
        <StatsOverview articles={newsArticles} />

        {/* Signals Section */}
        <SignalsSection signals={mockSignalsData} />

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

        <div className="flex gap-8">
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
            {isLoading ? (
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
                  <NewsCard key={article.id} article={article} />
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
    </div>
  );
};

export default Index;
