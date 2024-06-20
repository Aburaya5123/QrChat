FROM debian:latest AS builder

ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin"
RUN apt-get update && apt-get install -y gnupg software-properties-common apt-transport-https ca-certificates curl git gcc
RUN export NONINTERACTIVE=1 && \
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

RUN brew install kubectl && kubectl version --client
RUN brew tap hashicorp/tap && brew install hashicorp/tap/terraform
RUN brew install helm

FROM debian:latest

RUN apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg curl git gettext-base yq

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-sdk -y

COPY --from=builder /home/linuxbrew/.linuxbrew/bin/kubectl /usr/local/bin/kubectl
COPY --from=builder /home/linuxbrew/.linuxbrew/bin/terraform /usr/local/bin/terraform
COPY --from=builder /home/linuxbrew/.linuxbrew/bin/helm /usr/local/bin/helm
RUN chmod +x /usr/local/bin/kubectl /usr/local/bin/terraform /usr/local/bin/helm

WORKDIR /root/workspace

SHELL ["/bin/bash", "-c"]