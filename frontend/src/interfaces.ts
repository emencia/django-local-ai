interface FormError {
  message: string;
  code: string;
}

type FormErrors = Record<string, Array<FormError>>;

interface InferUsageContract {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

interface InferResponseContract {
  text: string;
  finish_reason: string;
  usage: InferUsageContract;
}

export {
  FormError,
  FormErrors,
  InferResponseContract,
}