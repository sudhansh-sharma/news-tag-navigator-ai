
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { TrendingUp, TrendingDown, ArrowRight, Clock } from 'lucide-react';

export interface Signal {
  id: string;
  type: 'buy' | 'sell' | 'entry';
  symbol: string;
  price: number;
  timestamp: string;
  confidence: 'high' | 'medium' | 'low';
  reason: string;
}

interface SignalCardProps {
  signal: Signal;
}

const SignalCard = ({ signal }: SignalCardProps) => {
  const getSignalIcon = (type: string) => {
    switch (type) {
      case 'buy':
        return <TrendingUp className="h-5 w-5 text-green-600" />;
      case 'sell':
        return <TrendingDown className="h-5 w-5 text-red-600" />;
      case 'entry':
        return <ArrowRight className="h-5 w-5 text-blue-600" />;
      default:
        return <ArrowRight className="h-5 w-5 text-gray-600" />;
    }
  };

  const getSignalColor = (type: string) => {
    switch (type) {
      case 'buy':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'sell':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'entry':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'high':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <Card className="hover:shadow-md transition-shadow duration-200 border border-gray-200">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {getSignalIcon(signal.type)}
            <div>
              <h3 className="font-semibold text-lg">{signal.symbol}</h3>
              <p className="text-sm text-gray-600">Rs {signal.price.toFixed(2)}</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <Clock className="h-4 w-4" />
            <span>{formatTime(signal.timestamp)}</span>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-3">
          <div className="flex gap-2">
            <Badge className={`text-xs font-semibold Rs {getSignalColor(signal.type)}`}>
              {signal.type.toUpperCase()}
            </Badge>
            <Badge className={`text-xs ${getConfidenceColor(signal.confidence)}`}>
              {signal.confidence.toUpperCase()} CONFIDENCE
            </Badge>
          </div>
          
          <p className="text-sm text-gray-700">{signal.reason}</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default SignalCard;
