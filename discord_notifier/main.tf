terraform {
  required_providers {
    discord-interactions = {
      source = "roleypoly/discord-interactions"
      version = "0.1.0"
    }
  }

  backend "local" {
    path = ".cache/terraform.tfstate"
  }
}

# AWS Provider
provider "aws" {
  region = "ap-northeast-1"
}

# Credentials from AWS
data "aws_ssm_parameter" "discord_application_id" {
  name = "/discord/minecraft_server/application-id"
}

data "aws_ssm_parameter" "discord_bot_token" {
  name            = "/discord/minecraft_server/token"
  with_decryption = true
}

# Discord Interaction Provider
provider "discord-interactions" {
  application_id = data.aws_ssm_parameter.discord_application_id.value
  bot_token      = data.aws_ssm_parameter.discord_bot_token.value
}

# Discord bot commands

resource "discord-interactions_global_command" "start" {
  name        = "start"
  description = "マインクラフトサーバーを起動します。"
}

resource "discord-interactions_global_command" "stop" {
  name        = "stop"
  description = "マインクラフトサーバーを停止します。"
}

resource "discord-interactions_global_command" "echo" {
  name        = "echo"
  description = "Echo message back to sender"

  option {
    name        = "message"
    description = "The message to echo back."
    type        = 3 # string
    required    = true
  }
}