from tools import schedule_event

if __name__ == "__main__":
    summary = "Test event from agent"
    start_time = "2025-07-02T15:00:00"
    result = schedule_event(summary, start_time)
    print(f"Result: {result}") 