import React from 'react';
import { Box, TextField, Grid, Typography, Card, CardContent } from '@mui/material';
import { AlgorithmParameter } from '../types/algorithm';

interface ParameterFormProps {
  parameters: AlgorithmParameter[];
  values: Record<string, string | number>;
  onChange: (name: string, value: string | number) => void;
}

export const ParameterForm: React.FC<ParameterFormProps> = ({
  parameters,
  values,
  onChange,
}) => {
  if (!parameters || parameters.length === 0) {
    return (
      <Box sx={{ py: 2 }}>
        <Typography color="textSecondary">No parameters to configure</Typography>
      </Box>
    );
  }

  return (
    <Card sx={{ width: '100%' }}>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Algorithm Parameters
        </Typography>
        <Grid container spacing={2}>
          {parameters.map((param) => (
            <Grid item xs={12} sm={6} key={param.name}>
              <TextField
                fullWidth
                label={param.name}
                type={param.type === 'float' ? 'number' : 'text'}
                value={values[param.name] || param.default}
                onChange={(e) => {
                  const value =
                    param.type === 'float'
                      ? parseFloat(e.target.value)
                      : param.type === 'integer'
                        ? parseInt(e.target.value)
                        : e.target.value;
                  onChange(param.name, value);
                }}
                inputProps={{
                  step: param.type === 'float' ? '0.01' : undefined,
                  min: param.min,
                  max: param.max,
                }}
                helperText={`${param.description}${
                  param.min && param.max ? ` (${param.min} - ${param.max})` : ''
                }`}
              />
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default ParameterForm;
