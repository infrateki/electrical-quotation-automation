# Generate Test Data for $ARGUMENTS

Generate comprehensive test data for development and testing:

1. **Analyze Requirements**
   - Determine what type of test data is needed
   - Identify data relationships and dependencies
   - Plan data volume and variety

2. **Generate Base Data**
   - Create company profiles (10-20 variations)
   - Generate project specifications
   - Create product catalog entries
   - Build contact lists

3. **Generate Quotation Scenarios**
   - Simple residential (10-50 line items)
   - Commercial buildings (100-200 line items)
   - Industrial facilities (200-500 line items)
   - Edge cases and error scenarios

4. **Populate Databases**
   ```python
   # PostgreSQL - Business data
   - Insert companies
   - Create users and permissions
   - Add quotation history
   
   # Neo4j - Product catalog
   - Create manufacturer nodes
   - Add product relationships
   - Build compatibility graph
   
   # Vector DB - Specifications
   - Generate embeddings
   - Add search indices
   ```

5. **Create Fixtures**
   - JSON fixtures for unit tests
   - SQL dumps for integration tests
   - Cypher scripts for graph data

6. **Validation**
   - Ensure referential integrity
   - Verify data distributions
   - Test edge cases

Output test data to `tests/fixtures/` directory.