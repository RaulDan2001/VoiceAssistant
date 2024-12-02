from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

class Assistant(object):
    def __init__(self):
        # Aleg un model pre-antrenat de pe Hugging Face pentru procesarea cuvintelor si raspuns
        #model_name = "EleutherAI/gpt-neo-2.7B"
        self.model_name = "gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

        #Aleg un model pre-antrenat de pe Hugging Face pentru traducere
        self.translate_model_name = "Helsinki-NLP/opus-mt-ROMANCE-en"
        print("Loading tokenizer...")
        self.translate_tokenizer = AutoTokenizer.from_pretrained(self.translate_model_name)
        print("Tokenizer loaded.")

        print("Loading model...")
        self.translate_model = AutoModelForSeq2SeqLM.from_pretrained(self.translate_model_name)
        print("Model loaded.")

        #Pentru traducere in romana
        self.ro_translate_model_name = "Helsinki-NLP/opus-mt-en-ROMANCE"
        print("Loading tokenizer...")
        self.ro_translate_tokenizer = AutoTokenizer.from_pretrained(self.ro_translate_model_name)
        print("Tokenizer loaded.")

        print("Loading model...")
        self.ro_translate_model = AutoModelForSeq2SeqLM.from_pretrained(self.ro_translate_model_name)
        print("Model loaded.")

        # Setez token-ul `pad` explicit (acesta va fi identic cu `eos`)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.translate_tokenizer.pad_token = self.translate_tokenizer.eos_token
        self.ro_translate_tokenizer.pad_token = self.ro_translate_tokenizer.eos_token

        
        
    def translate_to_english(self,text):
        # Tokenizez textul
        input_text = f"translate ro to en: {text}"
        inputs = self.translate_tokenizer(input_text, return_tensors="pt", padding=True)
        # Generez traducerea
        translated = self.translate_model.generate(input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=100,  # Ensure the translation output is long enough
        do_sample=False,
        num_beams=5,    # Using beam search for better translation quality
        early_stopping=True,
        pad_token_id=self.translate_tokenizer.pad_token_id,  # Explicit padding token id
        eos_token_id=self.translate_tokenizer.eos_token_id,  # Explicit EOS token id
        )
        # Decodific rezultatul
        result = self.translate_tokenizer.decode(translated[0], skip_special_tokens=True) 

        result = result.replace(f"translate ro to en: ", "").replace("<pad>", "").strip()
        return result

    def translate_to_romanian(self,text):
        #Tokenizez textul
        input_text = f"translate en to ro: {text}"
        inputs = self.ro_translate_tokenizer(input_text, return_tensors="pt", padding=True)
        #Generez traducerea
        translated = self.ro_translate_model.generate(input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=100,  # Ensure the translation output is long enough
        do_sample=False,
        num_beams=5,    # Using beam search for better translation quality
        early_stopping=True,
        pad_token_id=self.translate_tokenizer.pad_token_id,  # Explicit padding token id
        eos_token_id=self.translate_tokenizer.eos_token_id,  # Explicit EOS token id
        )

        # Decodific rezultatul
        result = self.translate_tokenizer.decode(translated[0], skip_special_tokens=True) 

        result = result.replace(f"translate ro to en: ", "").replace("<pad>", "").strip()
        return result

    def chat_with_assistant(self,prompt):
        # Convertesc întrebarea în formatul necesar pentru model
        translated_inputs = self.translate_to_english(prompt)
        print ("Translatet_input recevied=", translated_inputs)
        inputs = self.tokenizer(translated_inputs, return_tensors="pt", padding=True, truncation=True)
        # Accesez input_ids
        input_ids = inputs["input_ids"]

        # Generez un răspuns folosind parametrii pentru a evita repetitivitatea
        outputs = self.model.generate(
            input_ids,  # Tensorul corect
            max_new_tokens=50,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            attention_mask=inputs["attention_mask"],  # Adaug attention_mask
            do_sample=True,  # Activez sampling-ul
            top_k=50,  # Selecție restrictivă pentru cele mai probabile 50 de token-uri
            top_p=0.95,  # Nucleus sampling
            temperature=0.7,  # Temperatura mai mică reduce repetitivitatea
        )
    
        # Decodific răspunsul în text
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        #rezult = translate_to_romanian(response)
        return response

    def assistant_run(self):
        # Interacțiune continuă cu utilizatorul
        print("Salut de la asistent! Scrie exit pentru a ieși.")
        while True:
            user_input = input("Eu: ")
            if user_input.lower() == "exit":
                print("Asistent: La revedere!")
                break
            response = self.chat_with_assistant(user_input)
            print("Asistent:", response)
    


