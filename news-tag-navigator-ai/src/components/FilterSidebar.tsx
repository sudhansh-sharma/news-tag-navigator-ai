import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { X } from 'lucide-react';

interface FilterSidebarProps {
  sectors: string[];
  stocks: string[];
  selectedSectors: string[];
  selectedStocks: string[];
  selectedSentiment: string;
  onSectorsChange: (sectors: string[]) => void;
  onStocksChange: (stocks: string[]) => void;
  onSentimentChange: (sentiment: string) => void;
}

const FilterSidebar = ({
  sectors,
  stocks,
  selectedSectors,
  selectedStocks,
  selectedSentiment,
  onSectorsChange,
  onStocksChange,
  onSentimentChange,
}: FilterSidebarProps) => {
  const handleSectorChange = (sector: string, checked: boolean) => {
    if (checked) {
      onSectorsChange([...selectedSectors, sector]);
    } else {
      onSectorsChange(selectedSectors.filter(s => s !== sector));
    }
  };

  const handleStockChange = (stock: string, checked: boolean) => {
    if (checked) {
      onStocksChange([...selectedStocks, stock]);
    } else {
      onStocksChange(selectedStocks.filter(s => s !== stock));
    }
  };

  const clearAllFilters = () => {
    onSectorsChange([]);
    onStocksChange([]);
    onSentimentChange('');
  };

  const hasActiveFilters = selectedSectors.length > 0 || selectedStocks.length > 0 || selectedSentiment !== '';

  return (
    <div className="space-y-6">
      {/* Active Filters */}
      {hasActiveFilters && (
        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm">Active Filters</CardTitle>
              <Button variant="ghost" size="sm" onClick={clearAllFilters}>
                Clear All
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            {selectedSectors.map(sector => (
              <Badge key={`${sector}-sector`} variant="secondary" className="mr-1 mb-1">
                {sector}
                <button
                  onClick={() => handleSectorChange(sector, false)}
                  className="ml-1 hover:bg-gray-300 rounded-full p-0.5"
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            ))}
            {selectedStocks.map(stock => (
              <Badge key={`${stock}-stock`} variant="secondary" className="mr-1 mb-1">
                {stock}
                <button
                  onClick={() => handleStockChange(stock, false)}
                  className="ml-1 hover:bg-gray-300 rounded-full p-0.5"
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            ))}
            {selectedSentiment && (
              <Badge key={`${selectedSentiment}-sentiment`} variant="secondary" className="mr-1 mb-1">
                {selectedSentiment}
                <button
                  onClick={() => onSentimentChange('')}
                  className="ml-1 hover:bg-gray-300 rounded-full p-0.5"
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
          </CardContent>
        </Card>
      )}

      {/* Sentiment Filter */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Sentiment</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {['positive', 'negative', 'neutral'].map((sentiment) => (
            <div key={`${sentiment}-sentiment`} className="flex items-center space-x-2">
              <Checkbox
                id={sentiment}
                checked={selectedSentiment === sentiment}
                onCheckedChange={(checked) => onSentimentChange(checked ? sentiment : '')}
              />
              <label htmlFor={sentiment} className="text-sm capitalize cursor-pointer">
                {sentiment}
              </label>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Sectors Filter */}
      {sectors.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Sectors</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 max-h-64 overflow-y-auto">
            {sectors.map((sector) => (
              <div key={`${sector}-sector`} className="flex items-center space-x-2">
                <Checkbox
                  id={sector}
                  checked={selectedSectors.includes(sector)}
                  onCheckedChange={(checked) => handleSectorChange(sector, !!checked)}
                />
                <label htmlFor={sector} className="text-sm cursor-pointer">
                  {sector}
                </label>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Stocks Filter */}
      {stocks.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Stocks</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 max-h-64 overflow-y-auto">
            {stocks.map((stock) => (
              <div key={`${stock}-stock`} className="flex items-center space-x-2">
                <Checkbox
                  id={stock}
                  checked={selectedStocks.includes(stock)}
                  onCheckedChange={(checked) => handleStockChange(stock, !!checked)}
                />
                <label htmlFor={stock} className="text-sm font-mono cursor-pointer">
                  {stock}
                </label>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default FilterSidebar;
