import { ConsultationState } from "../types/consultation";

const API_URL = "http://localhost:8000";
const PHYSICIAN_REVIEW_TOKEN = "demo-physician-token";

export async function startConsultation(patientCase: string): Promise<ConsultationState> {
  const response = await fetch(`${API_URL}/consultation/start`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      patient_case: patientCase,
    }),
  });

  if (!response.ok) {
    throw new Error("Impossible de demarrer la consultation");
  }

  return response.json();
}

export async function resumeConsultation(params: {
  threadId: string;
  patientAnswer?: string;
  physicianTreatment?: string;
}): Promise<ConsultationState> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (params.physicianTreatment) {
    headers["X-Physician-Token"] = PHYSICIAN_REVIEW_TOKEN;
  }

  const response = await fetch(`${API_URL}/consultation/resume`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      thread_id: params.threadId,
      patient_answer: params.patientAnswer,
      physician_treatment: params.physicianTreatment,
    }),
  });

  if (!response.ok) {
    throw new Error("Impossible de reprendre la consultation");
  }

  return response.json();
}
