# Quiz & Notes Generator API

A production-ready FastAPI backend service that generates educational quizzes and study notes from PDF documents and audio lectures using OpenAI's GPT models and Whisper for audio transcription.

## 🚀 Features

- **Quiz Generation**: Create structured quizzes (MCQ, Multiple Choice, True/False) from PDF content
- **Notes Generation**: Synthesize comprehensive study notes from PDF materials and audio lectures
- **Audio Transcription**: Convert lecture audio to text using OpenAI Whisper
- **PDF Processing**: Extract and process text from PDF documents
- **Health Monitoring**: Built-in health check endpoints with system metrics
- **File Storage**: MongoDB GridFS integration for file management
- **Error Handling**: Comprehensive exception handling and logging
- **CORS Support**: Configurable cross-origin resource sharing

## 🏗️ Architecture

### Tech Stack
- **Framework**: FastAPI
- **Database**: MongoDB with MongoEngine ODM
- **AI/ML**: OpenAI GPT models, Whisper
- **File Processing**: PyMuPDF (fitz), python-multipart
- **Dependency Injection**: dependency-injector
- **Logging**: Python logging with rotation
- **Deployment**: Render.com ready

### Project Structure
```
app/
├── api/
│   ├── health/          # Health check endpoints
│   └── v1/              # API v1 routes
├── config/              # Configuration management
├── core/                # Core functionality (LLM, logging)
├── dependency/          # Dependency injection container
├── middlewares/         # Custom middlewares
├── schema/              # Pydantic models and database schemas
├── services/            # Business logic services
├── system_instructs/    # AI prompt templates
└── utils/               # Utility functions
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB instance
- OpenAI API key

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quiz-notes-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp example.env .env
   ```
   
   Update `.env` with your configuration:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   MONGO_DATABASE_NAME=your_database_name
   MONGO_DATABASE_HOST=mongodb://localhost:27017
   GPT_MODEL=gpt-3.5-turbo-1106  # or gpt-4o
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints

#### Health Check
```http
GET /
```
Returns server health metrics including memory usage, CPU load, and system information.

#### Create Notes
```http
POST /api/v1/notes/create
```
**Parameters:**
- `title` (form): Note title
- `description` (form): Note description  
- `pdf` (file): PDF document
- `audio` (file): Audio lecture file

**Response:**
```json
{
  "title": "string",
  "description": "string", 
  "audio": "file_id",
  "pdf": "file_id",
  "notes": "generated_notes_content"
}
```

#### Create Quiz
```http
POST /api/v1/quizes/create
```
**Parameters:**
- `prompt` (form): Quiz generation instructions
- `pdf` (file): PDF document

**Response:**
```json
{
  "prompt": "string",
  "pdf": "file_id",
  "questions": [
    {
      "_id": "q1",
      "question": "Question text",
      "type": "MCQ",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "marks": 5,
      "correct": 2
    }
  ]
}
```

### Question Types
- **MCQ**: Multiple choice with single correct answer
- **Multiple Correct**: Multiple choice with multiple correct answers
- **True/False**: Boolean questions
- **Open-Ended**: Free-form questions with grading instructions

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | ✅ |
| `MONGO_DATABASE_NAME` | MongoDB database name | - | ✅ |
| `MONGO_DATABASE_HOST` | MongoDB connection string | - | ✅ |
| `GPT_MODEL` | OpenAI model to use | `gpt-3.5-turbo-1106` | ❌ |
| `ALLOWED_ORIGINS` | CORS allowed origins | `["*"]` | ❌ |
| `ALLOWED_METHODS` | CORS allowed methods | `["*"]` | ❌ |
| `ALLOWED_HEADERS` | CORS allowed headers | `["*"]` | ❌ |

### MongoDB Setup
Ensure MongoDB is running and accessible. The application uses GridFS for file storage.

### OpenAI Models
Supported models:
- `gpt-3.5-turbo-1106` (default, cost-effective)
- `gpt-4o` (higher quality, more expensive)

## 🚀 Deployment

### Render.com Deployment
The application includes a `render.yaml` configuration for easy deployment on Render.com:

1. **Connect your repository** to Render
2. **Set environment variables** in Render dashboard
3. **Deploy** using the provided configuration

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations
- Use environment-specific settings
- Configure proper logging levels
- Set up monitoring and alerting
- Use a reverse proxy (nginx) for static files
- Configure database connection pooling
- Set up backup strategies for MongoDB

## 🔍 Monitoring & Logging

### Health Monitoring
The `/` endpoint provides comprehensive health metrics:
- System status
- Memory usage
- CPU utilization
- Server uptime

### Logging
- **Location**: `app/logs/`
- **Rotation**: 5MB per file, 3 backup files
- **Format**: Structured logging with timestamps
- **Levels**: INFO, ERROR, DEBUG

### Error Handling
- Global exception middleware
- Structured error responses
- Automatic retry for LLM failures
- Database connection error handling

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

### Test Coverage
- Unit tests for services
- Integration tests for API endpoints
- Mock external dependencies (OpenAI, MongoDB)

## 🔐 Security

### Best Practices Implemented
- Input validation using Pydantic
- File type validation
- Error message sanitization
- Environment variable configuration
- CORS configuration
- Request/response logging

### Security Considerations
- Store API keys securely
- Use HTTPS in production
- Implement rate limiting
- Validate file uploads
- Sanitize user inputs

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Add tests for new features
- Update documentation

## 📈 Performance

### Optimization Features
- Dependency injection for efficient resource management
- Instruction caching to avoid repeated file reads
- Connection pooling for database operations
- Async/await for non-blocking operations

### Scaling Considerations
- Horizontal scaling with load balancers
- Database sharding for large datasets
- Caching layer (Redis) for frequent requests
- CDN for static file delivery

## 🐛 Troubleshooting

### Common Issues

**MongoDB Connection Issues**
```bash
# Check MongoDB status
systemctl status mongod

# Verify connection string
mongo mongodb://localhost:27017
```

**OpenAI API Errors**
- Verify API key validity
- Check rate limits
- Monitor usage quotas

**File Upload Issues**
- Check file size limits
- Verify file format support
- Ensure proper permissions

### Logs Location
```bash
tail -f app/logs/app.log
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- **Issues**: GitHub Issues
- **Documentation**: API docs at `/docs`
- **Logs**: Check `app/logs/app.log`

---

## 🔄 Changelog

### v0.1.1 (Current)
- Initial release
- Quiz generation from PDF
- Notes generation from PDF + Audio
- Health monitoring
- MongoDB integration
- OpenAI integration

---

**Built with ❤️ using FastAPI**