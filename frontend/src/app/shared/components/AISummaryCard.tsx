import { Button } from 'flowbite-react';
import { Brain, Sparkles } from 'lucide-react';
import { formatFullDateTime } from '../../../lib/utils';

interface AISummaryCardProps {
  summary: string | null;
  isGenerating: boolean;
  generatedAt: string | null;
  onGenerate: () => void;
  showSummary: boolean;
  onToggleSummary: (show: boolean) => void;
}

export function AISummaryCard({
  summary,
  isGenerating,
  generatedAt,
  onGenerate,
  showSummary,
  onToggleSummary,
}: AISummaryCardProps) {
  return (
    <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4 mb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <Brain className="h-5 w-5 mr-2 text-purple-600" />
          <h4 className="text-sm font-medium text-purple-900 dark:text-purple-200">
            AI Ticket Summary
          </h4>
        </div>
        <Button
          size="sm"
          className="bg-orange-600 hover:bg-orange-700 focus:ring-orange-500"
          onClick={onGenerate}
          disabled={isGenerating}
        >
          <Sparkles className="h-4 w-4 mr-2" />
          {isGenerating ? 'Generating...' : (summary ? 'Regenerate Summary' : 'Generate Summary')}
        </Button>
      </div>

      {/* Loading state */}
      {isGenerating && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          <span className="ml-3 text-sm text-purple-700 dark:text-purple-300">
            AI is analyzing the ticket conversation...
          </span>
        </div>
      )}

      {/* Summary display */}
      {showSummary && summary && !isGenerating && (
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-purple-200 dark:border-purple-700 p-4">
          <div className="flex items-center justify-between mb-3">
            <h5 className="text-sm font-medium text-gray-900 dark:text-white">
              Summary Generated
            </h5>
            {generatedAt && (
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {formatFullDateTime(generatedAt)}
              </span>
            )}
          </div>
          <div className="prose prose-sm max-w-none dark:prose-invert">
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              {summary}
            </p>
          </div>
          <div className="flex justify-end mt-3">
            <Button
              size="xs"
              color="gray"
              onClick={() => onToggleSummary(false)}
            >
              Hide Summary
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

