import React, { useState } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  Tabs,
  Tab,
} from '@mui/material';
import { ResultsDisplay, TradeLog, ChartContainer } from '../components';
import { useResults, useTrades } from '../hooks';

interface ResultsPageProps {
  jobId?: string;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => (
  <div hidden={value !== index} style={{ width: '100%' }}>
    {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
  </div>
);

export const ResultsPage: React.FC<ResultsPageProps> = ({ jobId: initialJobId }) => {
  const [jobId, setJobId] = useState<string | undefined>(initialJobId || undefined);
  const [tabValue, setTabValue] = useState(0);
  const { results, loading, error } = useResults({ jobId });
  const { trades } = useTrades(jobId);

  const handleJobIdSubmit = (_e: React.FormEvent) => {
    _e.preventDefault();
    if (jobId && jobId.trim()) {
      setTabValue(1); // Switch to results tab
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ mb: 2, fontWeight: 'bold' }}>
          Backtest Results
        </Typography>
        <Typography color="textSecondary">
          View detailed backtest results, metrics, and trade log
        </Typography>
      </Box>

      {!jobId ? (
        <Paper sx={{ p: 3 }}>
          <form onSubmit={handleJobIdSubmit}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Enter Job ID
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                placeholder="e.g., 123e4567-e89b-12d3-a456-426614174000"
                value={jobId || ''}
                onChange={(e) => setJobId(e.target.value || undefined)}
                fullWidth
                size="small"
              />
              <Button variant="contained" type="submit">
                Fetch Results
              </Button>
            </Box>
          </form>
        </Paper>
      ) : (
        <>
          <Paper sx={{ mb: 3 }}>
            <Tabs value={tabValue} onChange={(_e, v: number) => setTabValue(v)}>
              <Tab label="Metrics" />
              <Tab label="Trade Log" />
              <Tab label="Capital Growth" />
            </Tabs>

            <TabPanel value={tabValue} index={0}>
              <ResultsDisplay results={results} loading={loading} error={error} />
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <TradeLog jobId={jobId as string | undefined} />
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              {results && trades.length > 0 ? (
                <ChartContainer trades={trades} initialCapital={results.initial_capital} />
              ) : (
                <Alert severity="info">No trades to display on chart.</Alert>
              )}
            </TabPanel>
          </Paper>
        </>
      )}
    </Container>
  );
};

export default ResultsPage;
