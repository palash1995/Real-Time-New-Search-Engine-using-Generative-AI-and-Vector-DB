class CommonDocument(BaseModel):
    article_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = Field(default_factory=lambda: "N/A")
    url: str = Field(default_factory=lambda: "N/A")
    published_at: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    source_name: str = Field(default_factory=lambda: "Unknown")
    image_url: Optional[str] = Field(default_factory=lambda: None)
    author: Optional[str] = Field(default_factory=lambda: "Unknown")
    description: Optional[str] = Field(default_factory=lambda: None)
    content: Optional[str] = Field(default_factory=lambda: None)

    @field_validator("title", "description", "content")
    def clean_text_fields(cls, v):
        if v is None or v == "":
            return "N/A"
        return clean_full(v)

    @field_validator("url", "image_url")
    def clean_url_fields(cls, v):
        if v is None:
            return "N/A"
        v = remove_html_tags(v)
        v = normalize_whitespace(v)
        return v

    @field_validator("published_at")
    def clean_date_field(cls, v):
        try:
            parsed_date = parser.parse(v)
            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            logger.error(f"Error parsing date: {v}, using current date instead.")

    @classmethod
    def from_json(cls, data: dict) -> "CommonDocument":
        """Create a CommonDocument from a JSON object."""
        return cls(**data)

    def to_kafka_payload(self) -> dict:
        """Prepare the common representation for Kafka payload."""
        return self.model_dump(exclude_none=False)