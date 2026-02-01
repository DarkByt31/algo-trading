import React, { useState } from 'react';
import {
  Box,
  Container,
  Paper,
  Grid,
  Typography,
  Divider,
  Alert,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import {
  StockSelector,
  AlgorithmSelector,
  ParameterForm,
  BacktestConfig,
  SubmitButton,
} from '../components';
import { useBacktest, useAlgorithms } from '../hooks';
import { BacktestRequest, BacktestParameters } from '../types/backtest';

interface BacktestPageProps {
  onBacktestSubmit?: (jobId: string) => void;
}

const formatDate = (date: Date): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const getDefaultDates = () => {
  const end = new Date();
  const start = new Date(end);
  start.setDate(start.getDate() - 10); // 10 days ago
  return {
    start: formatDate(start),
    end: formatDate(end),
  };
};

export const BacktestPage: React.FC<BacktestPageProps> = ({ onBacktestSubmit }) => {
  const { algorithms } = useAlgorithms();
  const { loading, error, submitBacktest, jobId } = useBacktest();

  const defaultDates = getDefaultDates();

  // Form state
  const [selectedStock, setSelectedStock] = useState('');
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('');
  const [startDate, setStartDate] = useState(defaultDates.start);
  const [endDate, setEndDate] = useState(defaultDates.end);
  const [capital, setCapital] = useState(50000);
  const [parameters, setParameters] = useState<Record<string, string | number>>({});
  const [activeStep, setActiveStep] = useState(0);

  // Get selected algorithm details
  const selectedAlgoDetails = algorithms.find((a) => a.id === selectedAlgorithm);

  // Initialize parameters when algorithm changes
  React.useEffect(() => {
    if (selectedAlgoDetails) {
      const defaultParams: Record<string, string | number> = {};
      selectedAlgoDetails.parameters.forEach((param) => {
        defaultParams[param.name] = param.default;
      });
      setParameters(defaultParams);
      setActiveStep(1); // Move to next step
    }
  }, [selectedAlgorithm, selectedAlgoDetails]);

  const handleParameterChange = (name: string, value: string | number) => {
    setParameters((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    if (!selectedStock || !selectedAlgorithm) {
      alert('Please select both stock and algorithm');
      return;
    }

    // Convert parameters to the correct type with uppercase keys
    const typedParameters: BacktestParameters = {
      SMA_WINDOW: Number(parameters.SMA_WINDOW || 20),
      Z_ENTRY: Number(parameters.Z_ENTRY || 1),
      Z_EXIT_THRESHOLD: Number(parameters.Z_EXIT_THRESHOLD || 0.3),
    };

    const request: BacktestRequest = {
      symbol: selectedStock,
      algorithm_id: selectedAlgorithm,
      start_date: startDate,
      end_date: endDate,
      initial_capital: capital,
      parameters: typedParameters,
      allow_short: true,
      brokerage_fee: 20.0,
    };

    try {
      const response = await submitBacktest(request);
      setActiveStep(2);
      onBacktestSubmit?.(response.job_id);
    } catch (err) {
      console.error('Failed to submit backtest:', err);
    }
  };

  const isFormValid = selectedStock && selectedAlgorithm;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ mb: 2, fontWeight: 'bold' }}>
          Backtest Strategy
        </Typography>
        <Typography color="textSecondary">
          Configure your trading strategy and run a backtest
        </Typography>
      </Box>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Stepper activeStep={activeStep}>
          <Step>
            <StepLabel>Select Stock & Algorithm</StepLabel>
          </Step>
          <Step>
            <StepLabel>Configure Parameters</StepLabel>
          </Step>
          <Step>
            <StepLabel>Results</StepLabel>
          </Step>
        </Stepper>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Strategy Configuration
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box>
                <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
                  Stock
                </Typography>
                <StockSelector value={selectedStock} onChange={setSelectedStock} />
              </Box>

              <Divider />

              <Box>
                <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
                  Algorithm
                </Typography>
                <AlgorithmSelector
                  value={selectedAlgorithm}
                  onChange={setSelectedAlgorithm}
                />
                {selectedAlgoDetails && (
                  <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                    {selectedAlgoDetails.description}
                  </Typography>
                )}
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <BacktestConfig
            startDate={startDate}
            endDate={endDate}
            capital={capital}
            onStartDateChange={setStartDate}
            onEndDateChange={setEndDate}
            onCapitalChange={setCapital}
          />
        </Grid>
      </Grid>

      {selectedAlgoDetails && (
        <Box sx={{ mt: 3 }}>
          <ParameterForm
            parameters={selectedAlgoDetails.parameters}
            values={parameters}
            onChange={handleParameterChange}
          />
        </Box>
      )}

      <Box sx={{ mt: 3 }}>
        <SubmitButton
          loading={loading}
          error={error || undefined}
          disabled={!isFormValid}
          onClick={handleSubmit}
        />
      </Box>

      {jobId && (
        <Alert severity="success" sx={{ mt: 3 }}>
          Backtest submitted successfully! Job ID: <strong>{jobId}</strong>
        </Alert>
      )}
    </Container>
  );
};

export default BacktestPage;
