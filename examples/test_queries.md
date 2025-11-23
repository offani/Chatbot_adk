# Test Queries for Multi-Agent System

This document contains test queries to verify the multi-agent system functionality.

## Web Search Queries

### Basic Factual Questions

```
Query: What is the capital of France?
Expected Agent: web_search_agent
Expected Response: Paris (with additional context)
```

```
Query: Who invented the telephone?
Expected Agent: web_search_agent
Expected Response: Alexander Graham Bell (with historical context)
```

### Current Events

```
Query: What's the latest news about artificial intelligence?
Expected Agent: web_search_agent
Expected Response: Recent AI-related news articles
```

```
Query: Current weather in Tokyo
Expected Agent: web_search_agent
Expected Response: Weather information for Tokyo
```

### General Knowledge

```
Query: How does photosynthesis work?
Expected Agent: web_search_agent
Expected Response: Explanation of photosynthesis process
```

```
Query: What are the main causes of climate change?
Expected Agent: web_search_agent
Expected Response: Scientific explanation with sources
```

## File Analysis Queries

### Image Analysis

```
Query: Describe what you see in this image
File: sample_image.jpg
Expected Agent: multimodal_agent
Expected Response: Detailed description of image content
```

```
Query: What colors are dominant in this picture?
File: sample_image.png
Expected Agent: multimodal_agent
Expected Response: Color analysis
```

### PDF Document Analysis

```
Query: Summarize this document
File: sample_document.pdf
Expected Agent: multimodal_agent
Expected Response: Concise summary of PDF content
```

```
Query: Extract the key points from this PDF
File: report.pdf
Expected Agent: multimodal_agent
Expected Response: Bullet-point list of key findings
```

### Spreadsheet Analysis

```
Query: Analyze the data in this spreadsheet
File: sample_data.xlsx
Expected Agent: multimodal_agent
Expected Response: Data insights and statistics
```

```
Query: What is the total in column B?
File: financial_data.csv
Expected Agent: multimodal_agent
Expected Response: Calculated total with context
```

### Text File Analysis

```
Query: What does this code do?
File: script.py
Expected Agent: multimodal_agent
Expected Response: Code explanation
```

```
Query: Summarize the content of this file
File: notes.txt
Expected Agent: multimodal_agent
Expected Response: Text summary
```

## Edge Cases & Error Handling

### Invalid File Paths

```
Query: Analyze this file
File: /nonexistent/path/file.pdf
Expected Result: Error message "File not found"
```

### Unsupported File Types

```
Query: Read this document
File: document.docx
Expected Result: Error message listing supported formats
```

### Empty Query

```
Query: [empty string]
Expected Result: "Please enter a valid query" message
```

### No File Provided for File Query

```
Query: Describe the image
File: [empty]
Expected Behavior: System attempts to handle gracefully or asks for file
```

## Ambiguous Routing Test Cases

### File-Related Query Without File

```
Query: Can you analyze Excel files?
File: [empty]
Expected Agent: Likely web_search_agent (general question)
OR multimodal_agent (capability question)
```

### Web Search with File Attached

```
Query: What is the current stock market status?
File: historical_data.xlsx
Expected Agent: web_search_agent (query is about current data, not file analysis)
Note: This tests whether the supervisor prioritizes query intent over file presence
```

## Complex Queries

### Multi-Step Reasoning

```
Query: Find information about quantum computing applications
File: [empty]
Expected Agent: web_search_agent
Expected Response: Multiple search results synthesized into coherent answer
```

### Contextual File Questions

```
Query: Based on this data, what trends do you see?
File: sales_data.csv
Expected Agent: multimodal_agent
Expected Response: Trend analysis based on spreadsheet content
```

## Conversation Flow Tests

### Follow-up Questions (Session Continuity)

```
Turn 1:
Query: What is machine learning?
Expected: Web search explanation

Turn 2:
Query: Tell me more about supervised learning
Expected: Web search with context from previous query
```

## Performance Test Queries

### Large File Handling

```
Query: Summarize this document
File: large_report.pdf (>10MB)
Expected: Should process without timeout errors
```

### Multiple Results Synthesis

```
Query: Compare renewable energy sources
Expected Agent: web_search_agent
Expected: Synthesis of multiple search results into comparative analysis
```

## Testing Instructions

### Manual Testing Steps

1. **Start the application**: `uv run python backend/main.py`
2. **Test each category**: Work through queries systematically
3. **Verify routing**: Check which agent handles each query
4. **Validate responses**: Ensure responses are accurate and relevant
5. **Test error handling**: Verify graceful failure for edge cases

### Expected Behavior Checklist

- [ ] Web search queries route to web_search_agent
- [ ] File analysis queries route to multimodal_agent
- [ ] File format validation works correctly
- [ ] Error messages are clear and helpful
- [ ] Session continuity maintained across turns
- [ ] No crashes or unhandled exceptions
- [ ] Responses are coherent and relevant
- [ ] Agent transfer happens transparently

### Success Criteria

✅ All basic queries work correctly  
✅ Routing decisions are intelligent and appropriate  
✅ Error handling is graceful and informative  
✅ File processing works for all supported formats  
✅ Web search returns relevant, synthesized information  
✅ No manual routing logic visible to user  
✅ System uses ADK's transfer mechanism successfully  

---

**Note**: Actual responses will vary based on current web search results and file content. The expected behaviors listed are general guidelines for validation.
