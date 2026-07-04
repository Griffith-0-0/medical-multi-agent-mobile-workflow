import { useState } from "react";
import { Alert, KeyboardAvoidingView, Platform, StyleSheet, Text, TextInput, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";

import { resumeConsultation } from "../api/consultationApi";
import { PrimaryButton } from "../components/PrimaryButton";
import { RootStackParamList } from "../navigation/AppNavigator";

type Props = NativeStackScreenProps<RootStackParamList, "PatientQuestions">;

export function PatientQuestionsScreen({ route, navigation }: Props) {
  const [consultation, setConsultation] = useState(route.params.consultation);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const questions = consultation.questions ?? [];
  const answers = consultation.patient_answers ?? [];
  const currentQuestion = questions[answers.length];
  const progress = Math.min(answers.length + 1, 5);

  async function handleAnswer() {
    if (!answer.trim()) {
      Alert.alert("Champ obligatoire", "Veuillez repondre a la question.");
      return;
    }

    try {
      setLoading(true);
      const updated = await resumeConsultation({
        threadId: consultation.thread_id,
        patientAnswer: answer.trim(),
      });

      setAnswer("");

      if (updated.needs_physician_review) {
        navigation.replace("PhysicianReview", { consultation: updated });
        return;
      }

      setConsultation(updated);
    } catch {
      Alert.alert("Erreur API", "Impossible d'envoyer la reponse patient.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : undefined}
      style={styles.container}
    >
      <View style={styles.content}>
        <View>
          <Text style={styles.progress}>Question {progress} / 5</Text>
          <Text style={styles.question}>{currentQuestion ?? "Preparation de la revue medecin..."}</Text>
        </View>

        <TextInput
          style={styles.input}
          placeholder="Votre reponse"
          placeholderTextColor="#94a3b8"
          value={answer}
          onChangeText={setAnswer}
          editable={!loading}
        />

        <PrimaryButton
          label={loading ? "Envoi..." : "Envoyer la reponse"}
          onPress={handleAnswer}
          disabled={loading || !currentQuestion}
        />
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8fafc",
  },
  content: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
    gap: 16,
  },
  progress: {
    color: "#2563eb",
    fontSize: 14,
    fontWeight: "700",
    marginBottom: 10,
  },
  question: {
    color: "#0f172a",
    fontSize: 24,
    fontWeight: "800",
    lineHeight: 31,
  },
  input: {
    minHeight: 52,
    borderWidth: 1,
    borderColor: "#cbd5e1",
    borderRadius: 8,
    backgroundColor: "#ffffff",
    paddingHorizontal: 14,
    color: "#0f172a",
    fontSize: 16,
  },
});
