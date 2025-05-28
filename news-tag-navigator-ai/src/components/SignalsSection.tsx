
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Signal as SignalIcon, TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';
import SignalCard, { Signal } from './SignalCard';

interface SignalsSectionProps {
  signals: Signal[];
}

const SignalsSection = ({ signals }: SignalsSectionProps) => {
  const buySignals = signals.filter(s => s.type === 'buy').length;
  const sellSignals = signals.filter(s => s.type === 'sell').length;
  const entrySignals = signals.filter(s => s.type === 'entry').length;

  const stats = [
    {
      label: 'Buy Signals',
      count: buySignals,
      icon: TrendingUp,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      label: 'Sell Signals',
      count: sellSignals,
      icon: TrendingDown,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      label: 'Entry Signals',
      count: entrySignals,
      icon: ArrowRight,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
  ];

  return (
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-6">
        <SignalIcon className="h-6 w-6 text-blue-600" />
        <h2 className="text-2xl font-bold text-gray-900">Trading Signals</h2>
      </div>

      {/* Signal Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {stats.map((stat) => (
          <Card key={stat.label} className="border border-gray-200">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.count}</p>
                </div>
                <div className={`p-2 rounded-full ${stat.bgColor}`}>
                  <stat.icon className={`h-5 w-5 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Signals List */}
      {signals.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {signals.map((signal) => (
            <SignalCard key={signal.id} signal={signal} />
          ))}
        </div>
      ) : (
        <Card className="p-8 text-center border border-gray-200">
          <SignalIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Signals Available</h3>
          <p className="text-gray-600">Trading signals will appear here when detected by the AI model.</p>
        </Card>
      )}
    </div>
  );
};

export default SignalsSection;
