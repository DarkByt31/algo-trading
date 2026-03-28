import React, { useState } from 'react';
import { Box, Container, AppBar, Toolbar, Tabs, Tab, Typography } from '@mui/material';
import { BacktestPage, ResultsPage } from './pages';
import './App.css';

export const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<0 | 1>(0);
  const [submittedJobId, setSubmittedJobId] = useState<string | undefined>();

  const handleBacktestSubmit = (jobId: string) => {
    setSubmittedJobId(jobId);
    setCurrentPage(1); // Switch to results page
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="sticky" sx={{ boxShadow: 1 }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            🔄 Trading Backtester
          </Typography>
        </Toolbar>
        <Toolbar variant="dense" sx={{ backgroundColor: '#f5f5f5', color: '#000' }}>
          <Tabs
            value={currentPage}
            onChange={(_, v) => setCurrentPage(v)}
            sx={{ flexGrow: 1 }}
            textColor="inherit"
          >
            <Tab label="Backtest" />
            <Tab label="Results" />
          </Tabs>
        </Toolbar>
      </AppBar>

      <Box component="main" sx={{ flex: 1, bgcolor: '#fafafa' }}>
        {currentPage === 0 && (
          <BacktestPage onBacktestSubmit={handleBacktestSubmit} />
        )}
        {currentPage === 1 && <ResultsPage jobId={submittedJobId} />}
      </Box>

      <Box component="footer" sx={{ py: 3, bgcolor: '#f5f5f5', borderTop: '1px solid #eee' }}>
        <Container maxWidth="lg">
          <Typography variant="caption" color="textSecondary">
            © 2026 Trading Backtester. All rights reserved.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default App;
