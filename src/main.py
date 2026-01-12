from .use_cases.resume_screening import screen_resume

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def main():
    resume_text = load_text("../data/sample_resume.txt")
    job_text = load_text("../data/sample_job_description.txt")

    score, fit, matched, missing = screen_resume(resume_text, job_text)

    print("\n📄 Resume Screening Result")
    print("----------------------------")
    print(f"Match Score: {score}%")
    print(f"Fit Category: {fit}")
    print(f"Matched Keywords: {sorted(matched)}")
    print(f"Missing Keywords: {sorted(missing)}")

if __name__ == "__main__":
    main()
