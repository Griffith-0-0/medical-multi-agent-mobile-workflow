import { useState } from "react";
import { Alert, KeyboardAvoidingView, Platform, StyleSheet, Text, TextInput, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";

import { startConsultation } from "../api/consultationApi";
import { PrimaryButton } from "../components/PrimaryButton";
import { RootStackParamList } from "../navigation/AppNavigator";

type Props = NativeStackScreenProps<RootStackParamList, "PatientCase">;

export function PatientCaseScreen({ navigation }: Props) {
  const [patientCase, setPatientCase] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleStart() {
    if (!patientCase.trim()) {
      Alert.alert("Champ obligatoire", "Veuillez saisir le cas initial patient.");
      return;
    }

    try {
      setLoading(true);
      const consultation = await startConsultation(patientCase.trim());
      navigation.navigate("PatientQuestions", { consultation });
    } catch {
      Alert.alert("Erreur API", "Verifier que le backend FastAPI est lance et accessible.");
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
        <Text style={styles.title}>Orientation clinique preliminaire</Text>
        <Text style={styles.description}>
          Saisis un cas patient simule. Le systeme posera ensuite 5 questions avant la revue medecin.
        </Text>

        <TextInput
          style={styles.input}
          multiline
          placeholder="Exemple: Patient de 28 ans avec toux et fievre depuis 2 jours."
          placeholderTextColor="#94a3b8"
          value={patientCase}
          onChangeText={setPatientCase}
          textAlignVertical="top"
        />

        <PrimaryButton
          label={loading ? "Demarrage..." : "Demarrer la consultation"}
          onPress={handleStart}
          disabled={loading}
        />

        <Text style={styles.disclaimer}>Ce systeme ne remplace pas une consultation medicale.</Text>
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
  title: {
    color: "#0f172a",
    fontSize: 28,
    fontWeight: "800",
    lineHeight: 34,
  },
  description: {
    color: "#475569",
    fontSize: 16,
    lineHeight: 23,
  },
  input: {
    minHeight: 170,
    borderWidth: 1,
    borderColor: "#cbd5e1",
    borderRadius: 8,
    backgroundColor: "#ffffff",
    padding: 14,
    color: "#0f172a",
    fontSize: 16,
    lineHeight: 22,
  },
  disclaimer: {
    color: "#64748b",
    fontSize: 13,
    lineHeight: 18,
  },
});
