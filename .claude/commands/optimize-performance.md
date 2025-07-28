# Optimize Performance for $ARGUMENTS

Analyze and optimize system performance:

1. **Profile Current Performance**
   ```python
   # Use cProfile for Python code
   # Monitor database query times
   # Track API response times
   # Measure memory usage
   ```

2. **Identify Bottlenecks**
   - Slow database queries
   - Inefficient algorithms
   - Excessive API calls
   - Memory leaks
   - Token usage spikes

3. **Database Optimization**
   - Add missing indexes
   - Optimize query patterns
   - Implement query caching
   - Use connection pooling
   - Batch operations

4. **Code Optimization**
   - Replace loops with vectorized operations
   - Use async/await properly
   - Implement lazy loading
   - Add memoization
   - Optimize data structures

5. **Caching Strategy**
   - Redis caching for catalog queries
   - In-memory caching for calculations
   - API response caching
   - Session state caching

6. **Token Optimization**
   - Compress context when possible
   - Use summaries for long content
   - Implement sliding window
   - Batch similar operations

7. **Parallel Processing**
   - Identify parallelizable tasks
   - Implement worker pools
   - Use message queues
   - Balance load across agents

Generate performance report with before/after metrics.