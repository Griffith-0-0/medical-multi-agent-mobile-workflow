import { useState } from "react";
import { Alert, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";

import { resumeConsultation } from "../api/consultationApi";
import { PrimaryButton } from "../components/PrimaryButton";
import { RootStackParamList } from "../navigation/AppNavigator";

type Props = NativeStackScreenProps<RootStackParamList, "PhysicianReview">;

export function PhysicianReviewScreen({ route, navigation }: Props) {
  const consultation = route.params.consultation;
  const [treatment, setTreatment] = useState("");
  const [loading, setLoading] = useState(false);
  const answers = consultation.patient_answers ?? [];

  async function handleValidate() {
    if (!treatment.trim()) {
      Alert.alert("Champ obligatoire", "Veuillez saisir la conduite a tenir du medecin.");
      return;
    }

    try {
      setLoading(true);
      const updated = await resumeConsultation({
        threadId: consultation.thread_id,
        physicianTreatment: treatment.trim(),
      });
      navigation.replace("FinalReport", { consultation: updated });
    } catch {
      Alert.alert("Erreur API", "Impossible de valider la revue medecin.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : undefined}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>Validation medecin</Text>

        <View style={styles.section}>
          <Text style={styles.label}>Synthese clinique preliminaire</Text>
          <Text style={styles.body}>
            Cas initial: {consultation.patient_case}
          </Text>
          <Text style={styles.body}>
            Le patient a repondu aux 5 questions d'orientation. La conduite a tenir doit etre validee par le medecin.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.label}>Reponses patient</Text>
          {answers.map((answer, index) => (
            <View key={`${answer}-${index}`} style={styles.answerRow}>
              <Text style={styles.answerIndex}>{index + 1}</Text>
              <Text style={styles.answerText}>{answer}</Text>
            </View>
          ))}
        </View>

        <View style={styles.section}>
          <Text style={styles.label}>Recommandation intermediaire</Text>
          <Text style={styles.body}>{consultation.interim_care}</Text>
        </View>

        <TextInput
          style={styles.input}
          multiline
          placeholder="Traitement ou conduite a tenir"
          placeholderTextColor="#94a3b8"
          value={treatment}
          onChangeText={setTreatment}
          textAlignVertical="top"
          editable={!loading}
        />

        <PrimaryButton
          label={loading ? "Validation..." : "Valider la revue"}
          onPress={handleValidate}
          disabled={loading}
        />
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8fafc",
  },
  content: {
    padding: 24,
    gap: 16,
  },
  title: {
    color: "#0f172a",
    fontSize: 26,
    fontWeight: "800",
    lineHeight: 32,
  },
  section: {
    borderWidth: 1,
    borderColor: "#e2e8f0",
    borderRadius: 8,
    backgroundColor: "#ffffff",
    padding: 14,
    gap: 8,
  },
  label: {
    color: "#334155",
    fontSize: 14,
    fontWeight: "800",
  },
  body: {
    color: "#475569",
    fontSize: 15,
    lineHeight: 22,
  },
  answerRow: {
    flexDirection: "row",
    gap: 10,
    alignItems: "flex-start",
  },
  answerIndex: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
    fontSize: 13,
    fontWeight: "800",
    lineHeight: 24,
    textAlign: "center",
  },
  answerText: {
    flex: 1,
    color: "#475569",
    fontSize: 15,
    lineHeight: 22,
  },
  input: {
    minHeight: 150,
    borderWidth: 1,
    borderColor: "#cbd5e1",
    borderRadius: 8,
    backgroundColor: "#ffffff",
    padding: 14,
    color: "#0f172a",
    fontSize: 16,
    lineHeight: 22,
  },
});
