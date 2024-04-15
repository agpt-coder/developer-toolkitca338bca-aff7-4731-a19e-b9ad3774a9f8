from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class DataPoint(BaseModel):
    """
    Represents a single unit of data or a parameter entry for the data processing. This structured approach allows for flexibility in the type of data being processed.
    """

    timestamp: datetime
    value: float
    parameters: Dict[str, str]


class ProcessedPoint(BaseModel):
    """
    Represents a single unit of processed data, providing insights or computed values derived from the initial dataset.
    """

    timestamp: datetime
    result: float
    insight: Optional[str] = None


class ProcessDataResponse(BaseModel):
    """
    The output model after processing the input data. This model provides a concise summary of the analysis, including any computed metrics, insights, or processed data.
    """

    summary: str
    processed_data: List[ProcessedPoint]
    analysis_duration: float


def process_data(data: List[DataPoint]) -> ProcessDataResponse:
    """
    Accepts data for processing and returns analysis results in real-time.

    This function is designed to process a series of data points represented by the DataPoint class. Each data point
    will be analyzed to compute a result and potentially derive insights based on its parameters. The function will
    aggregate these processed points into a ProcessDataResponse, summarizing the analysis and including details such as
    the individual processed points and the total duration of the process.

    Args:
        data (List[DataPoint]): A comprehensive representation of the data to be processed or parameters guiding how data processing should be conducted.

    Returns:
        ProcessDataResponse: The output model after processing the input data. This model provides a concise summary of the analysis, including any computed metrics, insights, or processed data.
    """
    start_time = datetime.now()
    processed_data = []
    for dp in data:
        processed_value = dp.value * 1.05
        insight = "No specific insight"
        if "key_metric" in dp.parameters:
            insight = (
                f"Key metric identified, parameter value: {dp.parameters['key_metric']}"
            )
        processed_data.append(
            ProcessedPoint(
                timestamp=dp.timestamp, result=processed_value, insight=insight
            )
        )
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    summary = f"Processed {len(data)} data points in {duration} seconds."
    return ProcessDataResponse(
        summary=summary, processed_data=processed_data, analysis_duration=duration
    )
