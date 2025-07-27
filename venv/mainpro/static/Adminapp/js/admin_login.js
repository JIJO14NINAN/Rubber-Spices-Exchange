// admin_login.js

function showSecretFields() {
            const normalFields = document.getElementById('normal-fields');
            const secretFields = document.getElementById('secret-fields');
            const secretToken = document.getElementById('id_secret_token');
            const hiddenAnswer = document.getElementById('id_hidden_answer');
            
            // Hide normal fields
            normalFields.classList.add('hidden');
            
            // Show secret fields and enable them
            secretFields.classList.remove('hidden');
            secretToken.classList.remove('hidden-field');
            hiddenAnswer.classList.remove('hidden-field');
            
            // Focus on the secret token field
            secretToken.focus();
        }

