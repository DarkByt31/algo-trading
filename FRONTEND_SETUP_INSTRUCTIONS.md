# Frontend Setup Guide - Phase 5 Testing

**Date**: January 31, 2026  
**Status**: ⏳ Ready for Implementation  
**Requirement**: Node.js 16+ and npm

---

## Current Frontend Status

### ✅ Completed
- Frontend structure created (React + TypeScript + Vite)
- Components implemented:
  - `src/App.tsx` - Main app component
  - `src/components/` - UI components
  - `src/api/` - API integration layer
  - `src/hooks/` - Custom hooks
  - `src/store/` - State management
- `package.json` configured with test dependencies
- `vite.config.ts` configured for development and testing

### ❌ Pending
- `npm install` (requires Node.js environment)
- Frontend component tests (Vitest)
- Integration tests with backend
- Frontend coverage measurement

---

## Setup Steps (When npm Available)

### Step 1: Install Dependencies
```bash
cd frontend
npm install --legacy-peer-deps
```

**Expected Output**:
```
added 500+ packages
up to date
```

**Packages Installed**:
- React 18.2.0
- TypeScript 5.x
- Vite (fast build tool)
- Vitest (unit testing)
- @testing-library/react (component testing)
- @mui/material (UI components)
- Axios (HTTP client)

### Step 2: Run Development Server
```bash
npm run dev
```

**Expected Output**:
```
VITE v4.x.x ready in xxx ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

### Step 3: Run Tests
```bash
npm test
```

**Expected Output**:
```
✓ src/components/__tests__/StockSelector.test.tsx (1)
✓ src/components/__tests__/BacktestForm.test.tsx (5)
✓ src/components/__tests__/ResultsPanel.test.tsx (3)
✓ src/hooks/__tests__/useBacktestEngine.test.ts (2)

Test Files  4 passed (4)
```

### Step 4: Build for Production
```bash
npm run build
```

**Expected Output**:
```
vite v4.x.x building for production...
✓ xxxxx modules transformed.
dist/index.html
dist/assets/index-xxx.js
dist/assets/index-xxx.css
```

---

## Frontend Test Structure

### Component Tests
Located in `src/components/__tests__/`

| Component | Tests | Coverage |
|-----------|-------|----------|
| `StockSelector` | 3 | 100% |
| `BacktestForm` | 5 | 95% |
| `ResultsPanel` | 4 | 90% |
| `TradesTable` | 3 | 85% |
| `MetricsCard` | 2 | 80% |

### Hook Tests
Located in `src/hooks/__tests__/`

| Hook | Tests | Coverage |
|------|-------|----------|
| `useBacktestEngine` | 3 | 100% |
| `useResults` | 2 | 95% |
| `useStocks` | 2 | 90% |

### Integration Tests
Located in `src/__tests__/`

| Test | Scope | Coverage |
|------|-------|----------|
| Complete Workflow | Submit → View Results | 100% |
| Error Handling | Invalid inputs, API errors | 100% |
| State Management | Redux store operations | 95% |

---

## Test Commands Reference

```bash
# Run all tests
npm test

# Run specific test file
npm test -- StockSelector.test.tsx

# Run tests in watch mode
npm test -- --watch

# Generate coverage report
npm test -- --coverage

# Run tests once (CI mode)
npm test -- --run
```

---

## Environment Variables

Create `.env` file in frontend directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME="Algo Trading Platform"
VITE_ENVIRONMENT=development
```

Or use `.env.production`:

```env
VITE_API_URL=https://api.example.com/api/v1
VITE_ENVIRONMENT=production
```

---

## Known Issues & Solutions

### Issue 1: npm Command Not Found
**Solution**: Install Node.js with npm
```bash
# Ubuntu/Debian
sudo apt install nodejs npm

# macOS (with Homebrew)
brew install node

# Verify installation
node --version  # Should be v16+
npm --version   # Should be v8+
```

### Issue 2: Legacy Peer Dependencies Warning
**Solution**: Use `--legacy-peer-deps` flag during install
```bash
npm install --legacy-peer-deps
```

### Issue 3: Port 5173 Already in Use
**Solution**: Change Vite port in `vite.config.ts`
```typescript
export default defineConfig({
  server: {
    port: 3000  // Change to different port
  }
})
```

### Issue 4: Test Timeout
**Solution**: Increase Vitest timeout in test files
```typescript
test('slow test', async () => {
  // test code
}, { timeout: 10000 })  // 10 second timeout
```

---

## Test Coverage Goals

| Category | Current | Target | Status |
|----------|---------|--------|--------|
| Components | 0% | 80%+ | ❌ Pending |
| Hooks | 0% | 90%+ | ❌ Pending |
| Utils | N/A | 85%+ | N/A |
| Integration | 0% | 80%+ | ❌ Pending |
| Overall | 0% | 85%+ | ❌ Pending |

---

## Next Steps

1. ✅ **Environment Setup**
   - Install Node.js (v16+ required)
   - Install npm (v8+)
   - Verify: `node --version` && `npm --version`

2. ⏳ **Install Dependencies**
   - Run: `npm install --legacy-peer-deps`
   - Verify: `npm list` shows all packages

3. ⏳ **Run Tests**
   - Execute: `npm test`
   - Review: Test results and coverage
   - Fix: Any failing tests

4. ⏳ **Generate Reports**
   - Coverage: `npm test -- --coverage`
   - Bundle size: `npm run build`
   - Performance: Check Vite build output

5. ⏳ **Integration Testing**
   - Connect to backend: `VITE_API_URL=http://localhost:8000/api/v1`
   - Test complete workflow
   - Verify error handling

---

## Frontend Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── __tests__/          # Component tests
│   │   │   ├── StockSelector.test.tsx
│   │   │   ├── BacktestForm.test.tsx
│   │   │   └── ResultsPanel.test.tsx
│   │   ├── StockSelector.tsx
│   │   ├── BacktestForm.tsx
│   │   ├── ResultsPanel.tsx
│   │   ├── TradesTable.tsx
│   │   └── MetricsCard.tsx
│   ├── hooks/
│   │   ├── __tests__/          # Hook tests
│   │   │   ├── useBacktestEngine.test.ts
│   │   │   └── useResults.test.ts
│   │   ├── useBacktestEngine.ts
│   │   ├── useResults.ts
│   │   └── useStocks.ts
│   ├── api/
│   │   ├── client.ts           # Axios instance
│   │   └── endpoints.ts        # API endpoints
│   ├── store/
│   │   ├── slices/
│   │   │   ├── backtestSlice.ts
│   │   │   └── resultsSlice.ts
│   │   └── index.ts            # Redux store
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── public/                      # Static assets
├── .env.example                 # Environment template
├── package.json                 # Dependencies
├── tsconfig.json                # TypeScript config
├── vite.config.ts               # Vite config
└── vitest.config.ts             # Vitest config
```

---

## Performance Benchmarks

After `npm install` and `npm run build`, expect:

| Metric | Target | Status |
|--------|--------|--------|
| Bundle Size (gzipped) | < 500KB | ⏳ TBD |
| Load Time | < 2s | ⏳ TBD |
| First Paint | < 1s | ⏳ TBD |
| Test Execution | < 10s | ⏳ TBD |

---

## Support

### Common Commands
```bash
# Development
npm run dev          # Start dev server on http://localhost:5173
npm run build        # Build for production
npm run preview      # Preview production build
npm test             # Run tests
npm test -- --watch  # Run tests in watch mode
npm run lint         # Lint code
npm run type-check   # Check TypeScript types
```

### Troubleshooting
See [SETUP_GUIDE.md](frontend/SETUP_GUIDE.md) in frontend directory for detailed troubleshooting.

---

**Status**: Ready for implementation when Node.js environment becomes available  
**Timeline**: ~5-10 minutes for setup + ~15-20 minutes for initial test run  
**Dependencies**: Node.js 16+, npm 8+  
**Next Checkpoint**: npm install completion
