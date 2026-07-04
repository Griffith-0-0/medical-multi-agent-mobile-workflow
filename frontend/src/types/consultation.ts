export type ConsultationState = {
    thread_id: string;
    patient_case?: string;
    questions?: string[];
    patient_answers?: string[];
    question_count?: number;
    diagnostic_summary?: string;
    interim_care?: string;
    physician_treatment?: string;
    final_report?: string;
    needs_physician_review?: boolean;
  };