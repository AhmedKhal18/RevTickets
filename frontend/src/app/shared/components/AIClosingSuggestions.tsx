'use client';

import { useState } from 'react';
import { Button, Card, Badge, Spinner } from 'flowbite-react';
import { Sparkles, CheckCircle, Copy } from 'lucide-react';
import type { ClosingCommentsResponse } from '../types';

interface AIClosingSuggestionsProps {
  ticketId: string;
  onApplySuggestion: (comment: string) => void;
  generateClosingComments: (ticketId: string) => Promise<ClosingCommentsResponse>;
}

export function AIClosingSuggestions({
  ticketId,
  onApplySuggestion,
  generateClosingComments,
}: AIClosingSuggestionsProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [suggestion, setSuggestion] = useState<ClosingCommentsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const result = await generateClosingComments(ticketId);
      setSuggestion(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate suggestions');
      setSuggestion(null);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleApply = () => {
    if (suggestion) {
      onApplySuggestion(suggestion.comment);
    }
  };

  return (
    <div className="space-y-3">
      {/* Generate Button */}
      {!suggestion && (
        <Button
          size="sm"
          color="light"
          className="w-full border-2 border-purple-200 hover:border-purple-300 dark:border-purple-700 dark:hover:border-purple-600"
          onClick={handleGenerate}
          disabled={isGenerating}
        >
          {isGenerating ? (
            <>
              <Spinner size="sm" className="mr-2" />
              Generating AI Suggestions...
            </>
          ) : (
            <>
              <Sparkles className="h-4 w-4 mr-2 text-purple-600 dark:text-purple-400" />
              Generate AI Closing Suggestions
            </>
          )}
        </Button>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}

      {/* Suggestion Display */}
      {suggestion && (
        <Card className="border-2 border-purple-200 dark:border-purple-700">
          <div className="space-y-3">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  AI Suggestion
                </h4>
              </div>
              <Badge color="purple" size="sm">
                AI Generated
              </Badge>
            </div>

            {/* Reason */}
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Reason for Closing:
              </label>
              <p className="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 p-2 rounded">
                {suggestion.reason}
              </p>
            </div>

            {/* Suggested Comment */}
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Suggested Closing Comment:
              </label>
              <p className="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 p-3 rounded whitespace-pre-wrap">
                {suggestion.comment}
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-2 pt-2">
              <Button
                size="sm"
                className="flex-1 bg-purple-600 hover:bg-purple-700 focus:ring-purple-500"
                onClick={handleApply}
              >
                <CheckCircle className="h-4 w-4 mr-2" />
                Apply Suggestion
              </Button>
              <Button
                size="sm"
                color="light"
                onClick={() => {
                  navigator.clipboard.writeText(suggestion.comment);
                }}
              >
                <Copy className="h-4 w-4" />
              </Button>
              <Button
                size="sm"
                color="light"
                onClick={() => setSuggestion(null)}
              >
                Regenerate
              </Button>
            </div>

            {/* Info Note */}
            <div className="text-xs text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-700">
              <p>💡 You can edit the suggestion before applying it to the closing comment.</p>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}

